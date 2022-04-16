import sys
import re
import spacy
import json
from company import Company
import editdistance

# load English language model
nlp = spacy.load('en_core_web_lg')

MIN_SCORE_FOR_COMPANY = 10 # minimum Elasticsearch score needed to be accepted as match
MIN_SCORE_FOR_COMPETITOR = 8.5 # minimum Elasticsearch score needed to be accepted as match
COMPETITION_SECTION_CHAR_LENGTH = 2500 # minimum length of text explored for competitors
LAST_CHAR = '.' # stop exploring text for competitors upon finding next instance of LAST_CHAR (set to '.' or '\n')
COMPETITOR_LABELS = ['ORG','PERSON'] # which spaCy NER labels to accept as potential competitors (e.g. 'ORG', 'PERSON', 'GPE', 'LOC', 'PRODUCT')
COMPANY_SIMILARITY_THRESHOLD = 0.7 # spaCy similarity score at which we consider two companies to be the same

# Creates Company object from the first line of the 10-K.
# First line of the 10-K must be formatted as:
# *#$#* <company_name>
def get_company(firstLine):
    assert firstLine[:5] == "*#$#*", "The 10-K does not begin with \"*#$#* <company_name>\"."
    nameFrom10K = firstLine[6:]
    return Company(nameFrom10K, minScore=MIN_SCORE_FOR_COMPANY)

# Find text of the Competition section
def get_competition_section(tenK):
    comps = [comp.start() for comp in re.finditer("\n *competition *\n", tenK, re.IGNORECASE)]
    assert len(comps), "Could not find Competition section."
    if len(comps) > 2:
        print("WARNING: multiple matches for Competition section, be skeptical of output.")
    beginning = tenK.find('\n', comps[-1] + 1, -1) + 1
    end = tenK.find(LAST_CHAR, beginning + COMPETITION_SECTION_CHAR_LENGTH, -1) + 1
    return tenK[beginning : end]

    ########################
    # Finds next heading if 10-K doesn't have random linebreaks
    ########################
    # nextHeading = None
    # if len(comps) > 1:
    #     text = tenK[comps[0] + 13 :]
    #     nextHeading = re.search("\n[a-zA-z]+[ a-zA-Z]*\n", text).group(0)[1:-1]

# Extracts competitors from Competition section
def get_competitors(text, company):
    # Named entities that have a match the Crunchbase database
    competitors = []
    competitor_ids = []
    
    # Named entities that don't have a match in the Crunchbase database
    leftovers = []
    leftover_names = []

    # Checks whether two Company objects refer to the same company
    def isSameCompany(company1, company2):
        # Check companyIDs if possible
        if company1.isInCrunchbase() and company2.isInCrunchbase():
            return company1.getCompanyID() == company2.getCompanyID()
        else:
            # Use spaCy similarity function if possible
            doc1 = nlp(company1.getNameFrom10K())
            doc2 = nlp(company2.getNameFrom10K())
            if doc1.vector_norm and doc2.vector_norm:
                return doc1.similarity(doc2) > COMPANY_SIMILARITY_THRESHOLD
            # Otherwise use simple edit distance measure
            else:
                doc1 = company1.getNameFrom10K().lower()
                doc2 = company2.getNameFrom10K().lower()
                return editdistance.eval(doc1, doc2) < len(doc2)

    text = text.replace('\n', ' ')
    doc = nlp(text)
    for sent in doc.sents:
        orgs = [ent for ent in sent.ents if ent.label_ in COMPETITOR_LABELS]
        for org in orgs:
            competitor = Company(org.text, context=sent.text, minScore=MIN_SCORE_FOR_COMPETITOR)
            if not isSameCompany(company, competitor):
                if competitor.isInCrunchbase() and competitor.getCompanyID() not in competitor_ids:
                    competitors.append(competitor)
                    competitor_ids.append(competitor.getCompanyID())
                elif competitor.getNameFrom10K() not in leftover_names:
                    leftovers.append(competitor)
                    leftover_names.append(competitor.getNameFrom10K())

    competitors = sorted(competitors, key=lambda competitor: competitor.getScore(), reverse=True)
    return (competitors, leftovers)

if __name__ == "__main__":
    out = {}
    tenK = sys.stdin.read()
    out['company'] = get_company(tenK[:tenK.find('\n')])
    competitionSection = get_competition_section(tenK)
    out['competitors'], out['leftovers'] = get_competitors(competitionSection, out['company'])
    
    # All necessary output is stored in the dictionary "out":
    # out['company'] -> the company that wrote the 10-K
    # out['competitors'] -> a list of Company objects for named entities found in Crunchbase
    # out['leftovers'] -> a list of Company objects for named entities NOT found in Crunchbase