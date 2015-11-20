PREFIX = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX bf: <http://bibframe.org/vocab/>
PREFIX kls: <http://knowledgelinks.io/external/resource/source/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>
"""

CONSTRUCT_GRAPH_PRE_URI = """CONSTRUCT
{
  ?s ?p ?o
}
WHERE
{
  """
  
CONSTRUCT_GRAPH_POST_URI = """  .
  {
    BIND (?s1 AS ?s) .
    ?s ?p ?o .
  } UNION {
    ?s1 ?p1 ?o1 .
	BIND (IF(ISBLANK(?o1),?o1,"") AS ?bn1) .
	?bn1 ?p2 ?o2 .
    BIND (?bn1 AS ?s) .
    BIND (?p2 AS ?p) .
    BIND (?o2 AS ?o) .
  } UNION {
    ?s1 ?p1 ?o1 .
	BIND (IF(ISBLANK(?o1),?o1,"") AS ?bn1) .
	?bn1 ?p2 ?o2 .
    BIND (IF(ISBLANK(?o2),?o2,"") AS ?bn2) .
    ?bn2 ?p3 ?o3 .
    BIND (?bn2 AS ?s) .
    BIND (?p3 AS ?p) .
    BIND (?o3 AS ?o) .
  } UNION {
    ?s1 ?p1 ?o1 .
	BIND (IF(ISBLANK(?o1),?o1,"") AS ?bn1) .
	?bn1 ?p2 ?o2 .
    BIND (IF(ISBLANK(?o2),?o2,"") AS ?bn2) .
    ?bn2 ?p3 ?o3 .
    BIND (IF(ISBLANK(?o3),?o3,"") AS ?bn3) .
    ?bn3 ?p4 ?o4 .
    BIND (?bn3 AS ?s) .
    BIND (?p4 AS ?p) .
    BIND (?o4 AS ?o) .
  } UNION {
    ?s1 ?p1 ?o1 .
	BIND (IF(ISBLANK(?o1),?o1,"") AS ?bn1) .
	?bn1 ?p2 ?o2 .
    BIND (IF(ISBLANK(?o2),?o2,"") AS ?bn2) .
    ?bn2 ?p3 ?o3 .
    BIND (IF(ISBLANK(?o3),?o3,"") AS ?bn3) .
    ?bn3 ?p4 ?o4 .
    BIND (IF(ISBLANK(?o4),?o4,"") AS ?bn4) .
    ?bn4 ?p5 ?o5 .
    BIND (?bn4 AS ?s) .
    BIND (?p5 AS ?p) .
    BIND (?o5 AS ?o) .
  }
"""
CONSTRUCT_GRAPH_PRE_LANG="""  BIND (DATATYPE(?o) AS ?DT) .
  FILTER(IF(!bound(?DT),TRUE,IF(?DT!=rdf:langString,TRUE,if(lang(?o)='"""
  	
CONSTRUCT_GRAPH_POST_LANG="""',TRUE,FALSE)))) ."""

CONSTRUCT_GRAPH_END="""}"""
