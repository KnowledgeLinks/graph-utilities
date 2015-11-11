__author__ = "Jeremy Nelson"

import argparse
import datetime
import requests
from sparql.general import *
from sparql.languages import workflow as languages


def execute_queries(queries, url):
    for i, sparql in enumerate(queries):
        result = requests.post(
            url,
            data={"query": sparql})
        if result.status_code > 399:
            print("..ERROR with {} for {}\n{}".format(
                sparql,
                url,
                result.text))
        else:
            print("{}.".format(i+1), end="")
        

def main(args):
    start = datetime.datetime.now()
    print("Starting {} Workflow at {}".format(
        args.workflow,
        start.isoformat()))
    if args.workflow.startswith("languages"):
        execute_queries(languages, args.triplestore)
    end = datetime.datetime.now()
    print("\nFinished {} Workflow at {}, total time={} min".format(
        end.isoformat(),
        args.workflow,
        (end-start).seconds / 60.0)) 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'workflow',
         choices=['languages'],
         help="Run SPARQL workflow, choices: languages")
    parser.add_argument(
        '--triplestore', 
        default="http://localhost:8080/bigdata",
        help="Triplestore URL")
    args = parser.parse_args()
    main(args)