from elasticsearch import Elasticsearch

# load Crunchbase database for Elasticsearching
es_client = Elasticsearch(
        'https://search-search-4cvp4pppu25hkg7aqrq2cfp3ya.us-east-1.es.amazonaws.com', maxsize=25
)

# Queries Crunchbase for matches of queryString using Elasticsearch
def crunchbase_query(queryString):
    term = 'company'
    searchParams = {
            "query": {
                "bool": {
                    "should": [{
                        "query_string": {
                            "query": queryString,
                            "fields": ['title']
                        }
                    }],
                    "filter": [{
                        "exists": {
                            "field": term + "ID"
                        }
                    }]
                }
            }
        }
    
    return es_client.search(index='companies', body=searchParams)

########################
# Structure of response:
########################
# response
# ↳ 'hits' – (dict)
#    ↳ 'max_score' : score of best hit – (float)
#    ↳ 'hits' – (list)
#       ↳ hit : any element of 'hits' – (dictionary)
#         ↳ '_id' : unclear, but not what we're looking for – (string)
#         ↳ '_score' : score indicating how good of a result it is – (float)
#         ↳ '_source'
#            ↳ 'uuid' : unique ID for company – (string)
#            ↳ 'title' : name of the company – (string)
#            ↳ 'industry' : comma-separated list of industry tags – (string)
#            ↳ 'companyID' : the company ID as stored in Neo4j – (string) USE THIS!!