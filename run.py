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
from sparql.subjects import workflow as subjects
from sparql import CONSTRUCT_GRAPH_PRE_URI
from sparql import CONSTRUCT_GRAPH_POST_URI
from sparql import CONSTRUCT_GRAPH_PRE_LANG
from sparql import CONSTRUCT_GRAPH_POST_LANG
from sparql import CONSTRUCT_GRAPH_END

# This is in-lue of a config file until such time it makes sense to create one  
def config():
   settings = {
       'triplestore':"http://localhost:9999/bigdata/sparql",
       'pulltype':"all",
       'format':'application/x-turtle',
       'filename':"default",
       'langpref':"all languages",
       'queryfile':"elasticsearchquery.rq",
       'es_url':'http://localhost:9200',
       'bulkactions':{                  
            '_op_type': 'create',
            '_index': 'bf',
            '_type': 'reference',
            '_id': ['field','resource']                       
            }
       }
   return settings
   
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

#This function will query the sparl endpoint and create those items in elasticsearch         
def push_dataToElasticsearch(args):
    #set initial args\parameters
    c = config()
    url = args.get('triplestore',c['triplestore'])            #URL to sparql endpoint of the triplestore
    esUrl = args.get('es_url',c['es_url'])                    #URL to elasticsearch
    qFile = args.get('queryfile',c['queryfile'])              #File containing the SPARQL query 
    mode = args.get('mode','normal')                          #Turn on debug mode
    aargs = args.get('bulkactions',c['bulkactions'])
    #************************* Bulkactions arg passing needs corrected *******************
    actionSettings = {                  
            '_op_type': aargs.get('_op_type',c['bulkactions']['_op_type']),
            '_index': aargs.get('_index',c['bulkactions']['_index']),
            '_type': aargs.get('_type',c['bulkactions']['_type']),
            '_id': aargs.get('_id',c['bulkactions']['_id'])                      
            }
    
    
    args.get('bulkactions',c['bulkactions']).get('_op_type',c['bulkactions']['_op_type']), #bulk update settings
    
    startSparql =datetime.datetime.now()  #Start a timer for the query portion
    print("Starting {} at {}".format(
        "SPARQL Query",
        startSparql.isoformat()))
    
    
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
        if actionSettings['_id'][0] == 'field':
            itemId = i[actionSettings['_id'][1]]['value'] 
        if mode != 'debug':
            jsonItem = json.loads('{'+i['obj']['value']+'}')  #convert SPARQL item result to json object
            actionItem = {  #create the action item to be pushed into es
                '_op_type': actionSettings['_op_type'],
                '_index': actionSettings['_index'],
                '_type': actionSettings['_type'],
                '_id': itemId,
                '_source': jsonItem                
            }
            actionList.append(actionItem) #add the item to the list of actions for the bulk loader
            #actionList.append(jsonItem)
        else:
            #if in debug mode post each item individually and print any errors
            print(total,". ",i['resource']['value'])
            lFile=(('{ "create" : { "_index" : "bf", "_type" : "reference", "_id" : "'+ i['resource']['value'] + '" } }\n'))
            lFile+=(('{'+i['obj']['value']+'}\n').encode())
            jsonItem = json.loads('{'+i['obj']['value']+'}')
            result = requests.post(esUrl + "/_bulk",
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
        es = Elasticsearch([esUrl])
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
    c=config()
    url = args.get('triplestore',c['triplestore'])
    pulltype = args.get('pulltype',c['pulltype'])  
    header_format = args.get('format',c['format'])
    fName = args.get('filename',c['filename'])
    langpref = args.get('langpref',c['langpref'])
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
        execute_queries(languages, args['triplestore'])
    if args['workflow'].startswith("subjects"):
        execute_queries(subjects, args['triplestore'])
    if args['workflow'].startswith("test"):
        test_queries(languages, args['triplestore'])
    if  args['workflow'].startswith("elastic"):
        push_dataToElasticsearch(args)
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
    c = config()
    parser=argparse.ArgumentParser()
    parser.add_argument(
        'workflow',
         choices=['languages', 'subjects', 'fedora','graph','elastic'],
         help="Run SPARQL workflow, choices: languages, subjects, fedora, graph, elastic")
    parser.add_argument(
        '--triplestore',
        default=c['triplestore'],
        help="Triplestore URL")
    parser.add_argument(
        '--pulltype',
        default=c['pulltype'],
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
        default=c['format'],
        help="Sets content-type for request in the header")
    parser.add_argument(
        '--filename',
        default=c['filename'],
        help="Specifies filename for output file, default from sparql header")
    parser.add_argument(
        '--langpref',
        default=c['langpref'],
        help="Enter the iso 639-1 two letter language code to return a graph with only that language")
    parser.add_argument(
        '--fedoraaction',
        default="test",
        help="Enter the actionpath")
    parser.add_argument(
        '--queryfile',
        default=c['queryfile'],
        help="File Containing the query to run")
    parser.add_argument(
        '--mode',
        default="normal",
        help="enter 'normal' or 'debug'")
    parser.add_argument(
        '--es_url',
        default=c['es_url'],
        help="enter 'normal' or 'debug'")
    parser.add_argument(
        '--bulkactions',
        default=c['bulkactions'],
        help="change bulk upload settings'")
    args=vars(parser.parse_args())
    main(args)
    

