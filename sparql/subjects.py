__author__ = "Mike Stabile"

from . import PREFIX
from sparql.general import *

SUBJECTS_CONVERT_RDF_TYPE = """#SUBJECTS_CONVERT_RDF_TYPE   
""" + PREFIX + """
DELETE
{
 ?subJId <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSCollection> ?rdfType  
}  

INSERT
{
  ?subjId a ?rdfType
}
WHERE
{
  ?subjId <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/authorities/subjects> .
  ?subjId <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSCollection> ?rdfType .
}"""

SUBJECTS_CHANGE_OWL_SAMEAS = """#SUBJECTS_CHANGE_OWL_SAMEAS 
""" + PREFIX + """
DELETE
{
 ?subjId <http://www.loc.gov/mads/rdf/v1#hasCloseExternalAuthority> ?owlsameAs  
}  
INSERT
{
  ?subjId owl:sameAs ?owlsameAs
}
WHERE
{
  ?subjId <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/authorities/subjects> .
  ?subjId <http://www.loc.gov/mads/rdf/v1#hasCloseExternalAuthority> ?owlsameAs .
}"""

SUBJECTS_CHANGE_TO_SKOS_BROADER = """#SUBJECTS_CHANGE_TO_SKOS_BROADER
""" + PREFIX + """
DELETE
{
 ?subjId <http://www.loc.gov/mads/rdf/v1#hasBroaderAuthority> ?broader 
}  
INSERT
{
  ?subjId skos:broader ?broader
}
WHERE
{
  ?subjId <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/authorities/subjects> .
  ?subjId <http://www.loc.gov/mads/rdf/v1#hasBroaderAuthority> ?broader .
}"""


SUBJECTS_CHANGE_TO_SKOS_NARROWER = """#SUBJECTS_CHANGE_TO_SKOS_NARROWER
""" + PREFIX + """
DELETE
{
 ?subjId <http://www.loc.gov/mads/rdf/v1#hasNarrowerAuthority> ?narrower 
}  
INSERT
{
  ?subjId skos:narrower ?narrower
}
WHERE
{
  ?subjId <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/authorities/subjects> .
  ?subjId <http://www.loc.gov/mads/rdf/v1#hasNarrowerAuthority> ?narrower .
}"""


CHANGE_TO_BF_LCC = """#CHANGE_TO_BF_LCC
""" + PREFIX + """
DELETE
{
 ?subjId <http://www.loc.gov/mads/rdf/v1#classification> ?lcc
}  
INSERT
{
  ?subjId bfe:lcc ?lcc
}
WHERE
{
  ?subjId <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/authorities/subjects> .
  ?subjId <http://www.loc.gov/mads/rdf/v1#classification> ?lcc .
}"""

CHANGE_TO_LCSH = """#CHANGE_TO_LCSH 
""" + PREFIX + """
DELETE
{
 ?subjId <http://id.loc.gov/vocabulary/identifiers/lccn> ?lcsh .
 ?subjId bfe:lcsh ?lcsh
}  
INSERT
{
  ?subjId bfe:lcsh ?lcsh
}
WHERE
{
  ?subjId <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/authorities/subjects> .
  ?subjId <http://id.loc.gov/vocabulary/identifiers/lccn> ?lcsh .
}"""

CHANGE_LISTS = """#CHANGE_LISTS
""" + PREFIX + """
DELETE
{
 ?subjId <http://www.loc.gov/mads/rdf/v1#elementList> ?list.
 ?subjId bfe:list ?list
}  
INSERT
{
  ?subjId bfe:list ?list
}
WHERE
{
  ?subjId <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/authorities/subjects> .
  ?subjId <http://www.loc.gov/mads/rdf/v1#elementList> ?list .
}
"""
REMOVE_ADMIN_METADATA = """#REMOVE_ADMIN_METADATA
""" + PREFIX + """
DELETE
{
 ?subjId <http://www.loc.gov/mads/rdf/v1#adminMetadata> ?admin
}  
WHERE
{
  ?subjId <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/authorities/subjects> .
  ?subjId <http://www.loc.gov/mads/rdf/v1#adminMetadata> ?admin .
}"""

REMOVE_EXAMPLE_NOTE = """#REMOVE_EXAMPLE_NOTE
""" + PREFIX + """
DELETE
{
 ?subjId <http://www.loc.gov/mads/rdf/v1#exampleNote> ?exp
}  
WHERE
{
  ?subjId <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/authorities/subjects> .
  ?subjId <http://www.loc.gov/mads/rdf/v1#exampleNote> ?exp .
}
"""

MERGE_URIs_FOR_LANGUAGES = """#MERGE_URIs_FOR_LANGUAGES
""" + PREFIX + """
DELETE {
  ?langid ?p ?o .
  ?sameAs ?p ?o .
}

INSERT
{
  ?langid ?p ?o
}
WHERE {
  ?langid a bf:Language .
  ?langid owl:sameAs ?sameAs .
  ?sameAs <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/authorities/subjects> .
  ?sameAs ?p ?o
}"""
UPDATE_SUBJECT_TYPE = """#UPDATE_SUBJECT_TYPE
""" + PREFIX + """
DELETE {
  ?id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/authorities/subjects> .
  ?id a bf:LocSubject.
}

INSERT
{
  ?id a bf:LocSubject
}
WHERE {
  ?id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/authorities/subjects> .
}"""

ADD_OWLSAMEAS_TAG_FOR_SUBJ_URI = """#ADD_OWLSAMEAS_TAG_FOR_SUBJ_URI
""" + PREFIX + """
DELETE
{
  ?subjId owl:sameAs ?subjId
}
INSERT 
{
  ?subjId owl:sameAs ?subjId
}
WHERE
{
  ?subjId a bf:LocSubject .
  OPTIONAL {?id2 owl:sameAs ?subjId.} .
  FILTER (!bound(?id2))
}"""
CHANGE_BASE_URI = """#CHANGE_BASE_URI
""" + PREFIX + """
DELETE
{ 
  ?subjId ?p ?o
}
INSERT
{
  ?baseURI ?p ?o
}
WHERE
{
  ?subjId a bf:LocSubject .
  BIND (URI(REPLACE(STR(?subjId),"http://id.loc.gov/authorities/subjects/","http://knowledgelinks.io/ns/bibcat/")) AS ?baseURI)
  ?subjId ?p ?o 
}"""

workflow = [
    SUBJECTS_CONVERT_RDF_TYPE,
    SUBJECTS_CHANGE_OWL_SAMEAS,
    SUBJECTS_CHANGE_TO_SKOS_BROADER,
    SUBJECTS_CHANGE_TO_SKOS_NARROWER,
    CHANGE_TO_BF_LCC,
    CHANGE_TO_LCSH,
    CHANGE_LISTS,
    REMOVE_ADMIN_METADATA,
    REMOVE_EXAMPLE_NOTE,
    MERGE_URIs_FOR_LANGUAGES, 
    UPDATE_SUBJECT_TYPE,
    ADD_OWLSAMEAS_TAG_FOR_SUBJ_URI,
    CHANGE_BASE_URI,
    CLEAN_UP_ORPHAN_BLANK_NODES,
    CLEAN_UP_ORPHAN_BLANK_NODES,
    CLEAN_UP_ORPHAN_BLANK_NODES
]
