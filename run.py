__author__="JeremyNelson"

import argparse
import datetime
import requests
import rdflib
import json
from sparql.general import*
from sparql.languages import workflow as languages
from sparql import CONSTRUCT_GRAPH_PRE_URI
from sparql import CONSTRUCT_GRAPH_POST_URI

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

#The below test query was to test directlinks one at a time for a service call to dbpedia
def test_queries(queries,url):
    result=requests.post(
        url,
        data={"query":"""PREFIX bf:<http://bibframe.org/vocab/>
PREFIX dbo:<http://dbpedia.org/ontology/>
PREFIX dbp:<http://dbpedia.org/property/>
PREFIX dbr:<http://dbpedia.org/resource/>
SELECT ?ref WHERE { ?bfLangId bf:dbpRef ?ref.}""",
        'format':'json'})
    uriItems=result.json().get('results').get('bindings')
    for uri in uriItems:
        qryStr="""PREFIX bf: <http://bibframe.org/vocab/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
SELECT * WHERE
{
SERVICE <http://DBpedia.org/sparql>
{
<"""+uri.get('ref').get('value')+""">rdfs:label?langLabel.
}.
}"""
        testUri=requests.post(
            url,
            data={"query":qryStr},
             headers={"Accept":"application/json"})
        print(uri.get('ref').get('value'),"|",testUri.status_code)
        print(qryStr)
        if testUri.status_code > 399:	
            print("Error")

def pull_graph(args):
    url = args.triplestore
    pulltype=args.get('pulltype','all')
    header_format=args.get('format','application/x-turtle')
    fName=args.get('filename','default')
    if pulltype=="resource":
        #use the resource uri to add to the query string to pull a singlegraph
        qstr="BIND(<"+args['resourceuri']+"> AS ?s1)"
    elif pulltype=="all":
        #usetheprovidestringfromthesparlselecttopullallofthegraphvalues.
        #thevariable?s1needstocontainalloftheresourcesthatyouwanttopull.
	#example:?s1abf:Languagepullsallofthelanguagegraphs
        qstr=args['sparqlselect']
        qstr=PREFIX+CONSTRUCT_GRAPH_PRE_URI+qstr+CONSTRUCT_GRAPH_POST_URI
    result=requests.post(
        url,
        data={"query":qstr},
        headers={"Accept":header_format}
    )
    if fName=='default':
        fName=result.headers.get('Content-disposition')[result.headers.get('Content-disposition').find("=")+1:]
    result.encoding='utf-8'
    with open(fName,"wb") as file_obj:
        file_obj.write(result.content)
    print("File saved as:{}".format(fName))
    if result.status_code>399:	
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
    end=datetime.datetime.now()
    print("\nFinished {} Workflow at {}, totaltime={} min".format(
        end.isoformat(),
        args.workflow,
        (end-start).seconds/60.0))

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument(
        'workflow',
        choices=['languages','test','graph'],
        help="Run SPARQL workflow, choices: languages,test,graph")
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
        help="Used when pulltype=resource, writes resourceURI as a string w/o <>")
    parser.add_argument(
        '--sparqlselect',
        help="""Used when pulltype=all, writes sparql triple to statement to
select resource.Var ?s1 must contain resourceURIs list""")
    parser.add_argument(
        '--format',
        default="application/x-turtle",
        help="Sets content-type for request in the header")
    parser.add_argument(
        '--filename',
        default="default",
        help="Specifies filename for output file, default from sparql header")
    args=parser.parse_args()
    main(args)
