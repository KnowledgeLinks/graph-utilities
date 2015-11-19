__author__="JeremyNelson, Mike Stabile"

import argparse
import datetime
import requests
import rdflib
import json
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

#The function will generate all of the fedora containers for the languages            
def create_fedoraContainers(url):
   result = requests.post(
        url,
        data={"query": PREFIX + """SELECT ?ref WHERE { ?bfLangId a bf:Language . BIND (STR(?bfLangId) as ?ref)}""",
        'format':'json'})
   uriItems = result.json().get('results').get('bindings')
   for uri in uriItems:
       #print(uri['ref']['value'])
       result = requests.put(uri['ref']['value'])

#This function will pull a graph from the triplestore based on a resource URI or a group of resource URIs
def pull_graph(args):
    url = args.triplestore  
    pulltype=args.pulltype  
    header_format=args.format
    fName=args.filename
    langpref = args.langpref
    returnType = 'file'
    
    if pulltype=="resource":
        #use the resource uri to add to the query string to pull a singlegraph
        qstr="BIND(<"+args.resourceuri+"> AS ?s1)"
    elif pulltype=="all":
        #use the string from the sparl select to pull all of the graph values.
        #the variable ?s1 needs to contain all of the resources that you want to pull.
        #example:   ?s1 a bf:Language      pulls all of the language graphs
        qstr=args.sparqlselect
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
        args.workflow,
        start.isoformat()))
    if args.workflow.startswith("languages"):
        execute_queries(languages, args.triplestore)
    if args.workflow.startswith("test"):
        test_queries(languages, args.triplestore)
    if  args.workflow.startswith("graph"):
        pull_graph(args)
    if args.workflow.startswith("fedora"):
        create_fedoraContainers(args.triplestore)
    end = datetime.datetime.now()
    print("\nFinished {} Workflow at {}, total time={} min".format(
        end.isoformat(),
        args.workflow,
        (end-start).seconds/60.0))

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument(
        'workflow',
         choices=['languages','fedora','graph'],
         help="Run SPARQL workflow, choices: languages, fedora, graph")
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
    args=parser.parse_args()
    main(args)
