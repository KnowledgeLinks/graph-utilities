__author__ = "Jeremy Nelson"

import argparse
import datetime
import requests
from sparql.general import *
from sparql.languages import workflow as languages


def execute_queries(queries, url):
    for i, sparql in enumerate(queries):
        print("{}.".format(i+1), end="")
        print(sparql[1:sparql.find('\n')])
        result = requests.post(
            url,
            data={"update": sparql})
        
        if result.status_code > 399:
            print("..ERROR with {} for {}\n{}".format(
                sparql,
                url,
                result.text))

#The below test query was to test direct links one at a time for a service call to dbpedia            
def test_queries(queries, url):
   result = requests.post(
        url,
        data={"query": """PREFIX bf: <http://bibframe.org/vocab/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
SELECT ?ref WHERE { ?bfLangId bf:dbpRef ?ref .}""",
        'format':'json'})
   uriItems = result.json().get('results').get('bindings')
   for uri in uriItems:
       qryStr = """PREFIX bf: <http://bibframe.org/vocab/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
SELECT * WHERE 
{ 
  SERVICE <http://DBpedia.org/sparql>
    { 
       <"""+ uri.get('ref').get('value') + """> rdfs:label ?langLabel.
    }.
}"""
       testUri = requests.post(
           url,
           data={"query": qryStr,
           'format':'json'})
       print(uri.get('ref').get('value') ," | " ,testUri.status_code)
       print(qryStr)
       if testUri.status_code > 399:    	
           print("Error")

 

def main(args):
    start = datetime.datetime.now()
    print("Starting {} Workflow at {}".format(
        args.workflow,
        start.isoformat()))
    if args.workflow.startswith("languages"):
        execute_queries(languages, args.triplestore)
    if args.workflow.startswith("test"):
        test_queries(languages, args.triplestore)
    end = datetime.datetime.now()
    print("\nFinished {} Workflow at {}, total time={} min".format(
        end.isoformat(),
        args.workflow,
        (end-start).seconds / 60.0)) 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'workflow',
         choices=['languages','test'],
         help="Run SPARQL workflow, choices: languages, test")
    parser.add_argument(
        '--triplestore', 
        default="http://localhost:9999/bigdata/sparql",
        help="Triplestore URL")
    args = parser.parse_args()
    main(args)
