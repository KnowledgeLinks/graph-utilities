__author__ = "Jeremy Nelson"

import argparse
import datetime
import requests
import rdflib
import json
from sparql.general import *
from sparql.languages import workflow as languages
from sparql.__init__ import CONSTRUCT_GRAPH_PRE_URI
from sparql.__init__ import CONSTRUCT_GRAPH_POST_URI

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
           data={"query": qryStr},
           headers={"Accept":"application/json"})
       print(uri.get('ref').get('value') ," | " ,testUri.status_code)
       print(qryStr)
       if testUri.status_code > 399:    	
           print("Error")

def pull_graph(graphargs, url):
   args = json.loads(graphargs.replace("'",'"'))
   if args['pulltype'] == "resource":
       #use the resourceuri to add to the query string to pull a single graph
	 	   QSTR = "BIND (<"+args['resourceuri'] +"> AS ?s1) "
   if args['pulltype'] == "all":
   	   #use the provide string from the sparl select to pull all of the graph values.
   	   #the variable ?s1 needs to contain all of the resources that you want to pull.
   	   #example:   ?s1 a bf:Language      pulls all of the language graphs
	 	   QSTR = args['sparqlselect']
   QSTR = PREFIX + CONSTRUCT_GRAPH_PRE_URI+ QSTR +CONSTRUCT_GRAPH_POST_URI
   result = requests.post(
       url,
       data={"query": QSTR},
       #args['format'] needs to be the header format for the rest API
       headers={"Accept":args['format']}
       )
   if args['filename'] == 'default':
   	   fName = result.headers.get('Content-disposition')[result.headers.get('Content-disposition').find("=")+1:]
   else:
       fName = args['filename']
   result.encoding = 'utf-8'
   file = open(fName, "wb")
   file.write(result.content)
   file.close()	
   print("File saved as: ",fName)

   if result.status_code > 399:    	
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
    if args.workflow.startswith("graph"):
        pull_graph(args.graphargs, args.triplestore)
    end = datetime.datetime.now()
    print("\nFinished {} Workflow at {}, total time={} min".format(
        end.isoformat(),
        args.workflow,
        (end-start).seconds / 60.0)) 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'workflow',
         choices=['languages','test','graph'],
         help="Run SPARQL workflow, choices: languages, test, graph")
    parser.add_argument(
        '--triplestore', 
        default="http://localhost:8080/bigdata/sparql",
        help="Triplestore URL")
    parser.add_argument(
        '--graphargs', 
        default="{'pulltype':'all','sparqlselect':'?s1 a bf:Language','format':'application/x-turtle','filename':'bibcatlanguages.ttl'}",
        help="""use json object notation; \nboth object and name must have quotes\n
            'pulltype': 'all'--write triple statement in 'sparqlselect'\n
                        'resource'--write resourceURI in the 'resourceURI' variable\n
                        
         'resourceuri':  used with 'pulltype'=resource -- write resourceURI as a string WITHOUT <>
         
        'sparqlselect':  used with 'pulltype'=all -- write the sparql triple to statment to select the 
                         the resources that you want.
                         variable ?s1 must contain the list of resource URIs
                         example: ?s1 rdf:type bf:Language   --will return all the language graphs
              'format':  Use the header value of the rest API of the desired outputtype 
                         Example: for turtle 'application/x-turtle'
                 
            'filename': 'default' will use the sparl header provided filename.
                         otherwise specify your own value
                         """)
    args = parser.parse_args()
    main(args)
