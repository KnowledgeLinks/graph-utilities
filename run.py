__author__="JeremyNelson, Mike Stabile"

import argparse
import datetime
import requests
import rdflib
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from sparql.general import*
from sparql.languages import workflow as languages
from sparql import CONSTRUCT_GRAPH_PRE_URI
from sparql import CONSTRUCT_GRAPH_POST_URI
from sparql import CONSTRUCT_GRAPH_PRE_LANG
from sparql import CONSTRUCT_GRAPH_POST_LANG
from sparql import CONSTRUCT_GRAPH_END

def execute_queries(queries,url):
    for i, sparql in enumerate(queries):
        print("{}.".format(i+1),end="")
        print(sparql[1:sparql.find('\n')])
        result=requests.post(
            url,
            data={"update":sparql})

        if result.status_code>399:
            print("..ERROR with {} for {}\n{}".format(
                sparql,
                url,
                result.text))

#This function will query blazegraph for            
def get_dataForEs(args):
    startSparql =datetime.datetime.now()  #Start a timer for the query portion
    print("Starting {} at {}".format(
        "SPARQL Query",
        startSparql.isoformat()))
    url = args['triplestore']
    qFile = args.get('queryfile','elasticsearchquery.rq')  #File containing the SPARQL query 
    mode = args.get('mode','normal')
    
    #read the query string file
    qFile_fo = open(qFile, encoding="utf-8")
    qStr = qFile_fo.read()
    qFile_fo.close()
    
    #run the query against the triplestore and store the results in esItems
    result = requests.post(
         url,
         data={"query": qStr,
         'format':'json'})
    esItems = result.json().get('results').get('bindings') 
    
    #end query timer    	
    endSparql = datetime.datetime.now()
    print("\nFinished {} at {}, total time={} seconds".format(
        "SPARQL query",
        endSparql.isoformat(),
        (endSparql-startSparql).seconds))
    
    #iterate over query results and build the elasticsearch actionList for bulk upload
    total = 0
    actionList = []
    for i in esItems:
        total = total + 1         
        if mode != 'debug':
            jsonItem = json.loads('{'+i['obj']['value']+'}')  #convert SPARQL item result to json object
            actionItem = {  #create the action item to be pushed into es
                '_op_type': 'create',
                '_index': 'bf',
                '_type': 'reference',
                '_id': i['resource']['value'], #_id is using the ?resource field from the query
                'doc': jsonItem  #doc contains the Json object
            }
            actionList.append(actionItem) #add the the item to the list of actions for the bulk loader
        else:
            #if in debug mode post each item individually and print any errors
            print(total,". ",i['resource']['value'])
            lFile=(('{ "create" : { "_index" : "bf", "_type" : "reference", "_id" : "'+ i['resource']['value'] + '" } }\n'))
            lFile+=(('{'+i['obj']['value']+'}\n').encode())
            jsonItem = json.loads('{'+i['obj']['value']+'}')
            result = requests.post("http://localhost:9200/_bulk",
                data = lFile)
            rNote = json.loads((result.content).decode())
            if rNote.get("errors"):
                item = rNote.get("items")[0]
                if item.get("create").get("status") != 409:
                    print(json.dumps(item.get("create")))
               
                                
    #push items to es using bulk helper
    if mode != 'debug': 
        print(total," items to post to elasticsearch")
        print("Now pushing into ElasticSearch")
        es = Elasticsearch(["http://localhost:9200"])
        helpers.bulk(
            es,
            actionList,
            stats_only=True
            )
    endEs = datetime.datetime.now()
    print("\nFinished {} at {}, total time={} seconds".format(
        "Processing and Pushing to Es",
        endEs.isoformat(),
        (endEs-endSparql).seconds))

#This function will generate a list of resource URIs as strings based on a filter for triples            
def get_referenceURIs(filterTriple,url):
   result = requests.post(
        url,
        data={"query": PREFIX + "SELECT ?sReturn WHERE { " +filterTriple + " . BIND (STR(?s) AS ?sReturn) }",
        'format':'json'})
   uriItems = result.json().get('results').get('bindings')
   returnlist = []
   for uri in uriItems:
       returnlist.append(uri['sReturn']['value'])
   return returnlist
   
#This function will generate the fedora resources
#*** graph subjects must already be encoded to the fedoraURIs
def generate_fedora_refs(tripleStoreURL,refType):
    if refType == "language":
        uriList = get_referenceURIs("?s a bf:Language",tripleStoreURL)
    if refType == 'test':
        uriList = ['http://localhost:8080/fedora/rest/ref/fre']
    print("There are ",len(uriList)," references to process.")
    i = 0
    for uri in uriList:
        i = i + 1
        print(i,". ",uri)
        args = {'triplestore':tripleStoreURL,
            'returntype': 'return',
            'resourceuri': uri}
        graph = pull_graph(args)
        graph_response = requests.put(uri,
            data=graph,
            headers={"Content-Type": "text/turtle"})

#This function will pull a graph from the triplestore based on a resource URI or a group of resource URIs
def pull_graph(args):
    url = args['triplestore']
    pulltype = args.get('pulltype','resource')  
    header_format = args.get('format','application/x-turtle')
    fName = args.get('filename','default')
    langpref = args.get('langpref','all languages')
    returnType = args.get('returntype','file')

    if pulltype=="resource":
        #add the resource uri to the query string to pull a single graph
        qstr="BIND(<"+args['resourceuri']+"> AS ?s1)"
    elif pulltype=="all":
        #use the string from the sparl select to pull all of the graph values.
        #the variable ?s1 needs to contain all of the resources that you want to pull.
        #example:   ?s1 a bf:Language      pulls all of the language graphs
        qstr=args['sparqlselect']
    qstr=PREFIX+CONSTRUCT_GRAPH_PRE_URI+qstr+CONSTRUCT_GRAPH_POST_URI
    
    #langpref allows you to display the graph only in one language. 
    if langpref == 'all languages':
        qstr=qstr+CONSTRUCT_GRAPH_END
    else:
        qstr=qstr+CONSTRUCT_GRAPH_PRE_LANG+langpref+CONSTRUCT_GRAPH_POST_LANG+CONSTRUCT_GRAPH_END
   
    #send query to triplestore
    result=requests.post(
        url,
        data={"query":qstr},
        headers={"Accept":header_format}
    )
    
    #process results as file or return the contents to the calling function
    if returnType == 'file':
        if fName=='default':
            fName=result.headers.get('Content-disposition')[result.headers.get('Content-disposition').find("=")+1:]
        result.encoding='utf-8'
        with open(fName,"wb") as file_obj:
            file_obj.write(result.content)
        print("File saved as:{}".format(fName))
    elif returnType == 'return':
        return result.content
        
    #print any error codes    
    if result.status_code>399:	
        print(qstr)
        print("Error{}\n{}".format(result.status_code,result.text))
      
def main(args):
    start=datetime.datetime.now()
    print("Starting {} Workflow at {}".format(
        args['workflow'],
        start.isoformat()))
    if args['workflow'].startswith("languages"):
        execute_queries(languages, args.triplestore)
    if args['workflow'].startswith("test"):
        test_queries(languages, args.triplestore)
    if  args['workflow'].startswith("elastic"):
        get_dataForEs(args)
    if  args['workflow'].startswith("graph"):
        pull_graph(args)
    if args['workflow'].startswith("fedora"):
        generate_fedora_refs(args['triplestore'],args['fedoraaction'])
    end = datetime.datetime.now()
    print("\nFinished {} Workflow at {}, total time={} min".format(
        end.isoformat(),
        args['workflow'],
        (end-start).seconds/60.0))

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument(
        'workflow',
         choices=['languages','fedora','graph','elastic'],
         help="Run SPARQL workflow, choices: languages, fedora, graph, elastic")
    parser.add_argument(
        '--triplestore',
        default="http://localhost:8080/bigdata/sparql",
        help="Triplestore URL")
    parser.add_argument(
        '--pulltype',
        default="all",
        help="Write triple statement or resourceURI",
        choices=["all","resource"])
    parser.add_argument(
        '--resourceuri',
        help="Used when pulltype=resource, enter the resourceURI as a string w/o <>")
    parser.add_argument(
        '--sparqlselect',
        help="""Used when pulltype=all, enter the sparql triple statement to
                select the desired resources. Var ?s1 must resolve to the resourceURI list""")
    parser.add_argument(
        '--format',
        default="application/x-turtle",
        help="Sets content-type for request in the header")
    parser.add_argument(
        '--filename',
        default="default",
        help="Specifies filename for output file, default from sparql header")
    parser.add_argument(
        '--langpref',
        default="all languages",
        help="Enter the iso 639-1 two letter language code to return a graph with only that language")
    parser.add_argument(
        '--fedoraaction',
        default="test",
        help="Enter the actionpath")
    parser.add_argument(
        '--queryfile',
        default="elasticsearchquery.rq",
        help="File Containing the query to run")
    parser.add_argument(
        '--bulksavefile',
        default="es_bulk_save.txt",
        help="filename to save the file for bulk elasticsearch upload")
    parser.add_argument(
        '--mode',
        default="normal",
        help="enter 'normal' or 'debug'")
    args=vars(parser.parse_args())
    main(args)