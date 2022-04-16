from resultid_es_query import crunchbase_query

class Company:

    ###############################################################
    # nameFrom10K: string of the company's name as it appears in 
    #              the 10K file.
    # context:     string of the sentence in which the company is
    #              mentioned in the 10K file (for competitors only).
    # minscore:    int/float of the minimum Elasticsearch score needed
    #              to be considered a correct match in the database.
    ###############################################################
    def __init__(self, nameFrom10K, context = None, minScore = 10):
        self._nameFrom10K = nameFrom10K
        self._context = context

        topHit = crunchbase_query(nameFrom10K)['hits']['hits'][0]
        if topHit['_score'] > minScore:
            self._inCrunchbase = True
            self._companyID = topHit['_source']['companyID']
            self._companyName = topHit['_source']['title']
            self._score = topHit['_score']
        else:
            self._inCrunchbase = False
            self._companyName, self._companyName, self._score = (None, None, None)
            if not context: print("WARNING: No company match found in Crunchbase for {}.".format(nameFrom10K))
    
    # Returns company name as mentioned in the 10-K file
    def getNameFrom10K(self):
        return self._nameFrom10K
    
    # Returns the sentence in the 10-K containing the company mention (if competitor)
    def getContext(self):
        return self._context

    # Returns True if Crunchbase match was found, False otherwise
    def isInCrunchbase(self):
        return self._inCrunchbase
    
    # Returns companyID as found in Crunchbase
    def getCompanyID(self):
        if not self._inCrunchbase:
            print("WARNING: companyID not available (no Crunchbase match).")
        return self._companyID

    # Returns companyName as found in Crunchbase
    def getCompanyName(self):
        if not self._inCrunchbase:
            print("WARNING: companyName not available (no Crunchbase match).")
        return self._companyName

    # Returns score
    def getScore(self):
        if not self._inCrunchbase:
            print("WARNING: score not available (no Crunchbase match).")
        return self._score
    
    # Prints out information about Company object
    def printOut(self):
        print("-----------------------------------------")
        print("Match in Crunchbase? --> " + str(self._inCrunchbase))
        if self._inCrunchbase:
            print("\tcompanyName: " + self._companyName)
            print("\tcompanyID: " + self._companyID)
            print("\tscore: " + str(self._score))
        print("Info from 10-K:")
        print("\tnameFrom10K: " + self._nameFrom10K)
        if self._context:
            print("\tcontext: " + self._context)
        print("-----------------------------------------\n")