PREFIX = """prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix skos: <http://www.w3.org/2004/02/skos/core#>
prefix bf: <http://bibframe.org/vocab/>
prefix klb: <http://knowledgelinks.io/ns/bibcat/>
prefix dbo: <http://dbpedia.org/ontology/>
prefix dbp: <http://dbpedia.org/property/>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix sesame: <http://www.openrdf.org/schema/sesame#>
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
prefix fn: <http://www.w3.org/2005/xpath-functions#>
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix dc: <http://purl.org/dc/elements/1.1/>
prefix hint: <http://www.bigdata.com/queryHints#>
prefix bd: <http://www.bigdata.com/rdf#>
prefix bds: <http://www.bigdata.com/rdf/search#>
prefix bfe: <http://bibframe.org/extensions/>
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
