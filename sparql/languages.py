__author__ = "Mike Stabile"

from . import PREFIX
from sparql.general import *

ADD_ISO6391_TO_RDF_TYPE_AND_DELETE_EXTRA_FIELDS = """#ADD_ISO6391_TO_RDF_TYPE_AND_DELETE_EXTRA_FIELDS
""" + PREFIX + """
DELETE
{
  ?langid <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSCollection>	<http://id.loc.gov/vocabulary/iso639-1/collection_iso639-1>	.
  ?langid <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSCollection>	<http://id.loc.gov/vocabulary/iso639-1/collection_PastPresentISO639-1Entries> .
  ?langid <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/vocabulary/iso639-1>	.
  ?langid rdf:type	<http://www.loc.gov/mads/rdf/v1#Authority>	.
  ?langid rdf:type	<http://www.loc.gov/mads/rdf/v1#Language> .	
  ?langid rdf:type	rdf:Resource	.
  ?langid rdf:type	<http://id.loc.gov/vocabulary/iso639-1/iso639-1_Language> .
}
INSERT
{
  ?bfLangURI a <http://id.loc.gov/vocabulary/iso639-1/iso639-1_Language> .
  ?bfLangURI a <http://id.loc.gov/vocabulary/iso639-1> .
  ?bfLangURI bfe:iso6391 ?langCode .
}
WHERE
{
  ?bfLangURI a	bf:Language .
  ?langid a  <http://id.loc.gov/vocabulary/iso639-1/iso639-1_Language> .
  ?bfLangURI owl:sameAs ?langid .
  ?langid <http://www.loc.gov/mads/rdf/v1#hasExactExternalAuthority> ?langURI .
  ?langid <http://www.loc.gov/mads/rdf/v1#code> ?langCode .
}"""

ADD_ISO6392_LINKAGE_FROM_ISO6391_RDF_FILE = """#ADD_ISO6392_LINKAGE_FROM_ISO6391_RDF_FILE
""" + PREFIX + """
DELETE
{
  ?langid <http://www.loc.gov/mads/rdf/v1#hasExactExternalAuthority> ?langURI
}
INSERT
{
	?bfLangURI owl:sameAs ?langURI
}
WHERE
{
     <http://id.loc.gov/vocabulary/iso639-1> <http://www.loc.gov/mads/rdf/v1#hasTopMemberOfMADSScheme> ?langid.
	 ?bfLangURI a	bf:Language .
  ?bfLangURI owl:sameAs ?langid .
  ?langid <http://www.loc.gov/mads/rdf/v1#hasExactExternalAuthority> ?langURI .
}"""

COPY_NOTES_FROM_ISO_6391 = """#COPY_NOTES_FROM_ISO_6391
""" + PREFIX + """
DELETE
{
  ?langid	<http://www.loc.gov/mads/rdf/v1#historyNote> ?note .
}
INSERT
{
  ?langid bf:note ?fnote .
}
WHERE
{
    <http://id.loc.gov/vocabulary/iso639-1> <http://www.loc.gov/mads/rdf/v1#hasTopMemberOfMADSScheme> ?langid.
	?langid ?p ?o .
   	<http://id.loc.gov/vocabulary/iso639-1> <http://www.loc.gov/mads/rdf/v1#hasTopMemberOfMADSScheme> ?langid.
  	?langid	<http://www.loc.gov/mads/rdf/v1#historyNote> ?note .
  	BIND (CONCAT("ISO 639-1: ",?note) AS ?fnote) .
	?bfLangURI a	bf:Language .
    ?bfLangURI owl:sameAs ?langid .
}"""


DELETE_LANGUAGE_NOTES = """#DELETE_LANGUAGE_NOTES
""" + PREFIX + """
DELETE
{
  ?langid <http://www.loc.gov/mads/rdf/v1#editorialNote> ?note .
}
WHERE
{
  ?langid a bf:Language .
  ?langid <http://www.loc.gov/mads/rdf/v1#editorialNote> ?note .
}"""


DELETE_MADS_ADMIN_METADATA = """#DELETE_MADS_ADMIN_METADATA
""" + PREFIX + """
DELETE
{
  ?langid <http://www.loc.gov/mads/rdf/v1#adminMetadata> ?adminObject .
}
WHERE
{
  ?langid a bf:Language .
  ?langid <http://www.loc.gov/mads/rdf/v1#adminMetadata> ?adminObject .
}"""

INSERT_DBPEDIA_ABSTRACTS_OWL = """#INSERT_DBPEDIA_ABSTRACTS_OWL 
""" + PREFIX + """
DELETE
{
  ?bfLangId bf:summary ?summary
}
INSERT
{?bfLangId bf:summary ?summary}
WHERE
{

  	{
      ?bfLangId a bf:Language .
      ?bfLangId owl:sameAs ?p .
      FILTER (STRSTARTS(STR(?p),"http://dbpedia.org/resource/"))
      
     }
	SERVICE <http://DBpedia.org/sparql>
	{ 
      ?p dbo:abstract ?summary. 
    }

}"""

INSERT_DBPEDIA_ABSTRACTS = """#INSERT_DBPEDIA_ABSTRACTS 
""" + PREFIX + """
DELETE
{
  ?bfLangId bf:summary ?summary .
}
INSERT
{
  ?bfLangId bf:summary ?summary .
}
WHERE 
{

  ?bfLangId a bf:Language .
  ?bfLangId dbo:wikiPageID ?wiki .

  SERVICE <http://DBpedia.org/sparql>
    { 
      ?dbPediaResource a dbo:Language .
      ?dbPediaResource dbo:wikiPageID  ?wiki .
      ?dbPediaResource dbo:abstract ?summary .
    }
}
"""
INSERT_DBPEDIA_ABSTRACTS_2 = """#INSERT_DBPEDIA_ABSTRACTS_2
""" + PREFIX + """
DELETE
{
  ?bfLangId bf:summary ?summary .
}
INSERT
{
  ?bfLangId bf:summary ?summary .
}
WHERE 
{

  OPTIONAL {
    ?bfLangId a bf:Language .
    ?bfLangId dbo:wikiPageID ?wiki .
    OPTIONAL {?bfLangId bf:summary ?sum} .
    filter (!bound(?sum))
  }
  SERVICE <http://DBpedia.org/sparql>
    { 
      ?dbPediaResource dbo:wikiPageID  ?wiki .
      ?dbPediaResource dbo:abstract ?summary .
    }

}"""
INSERT_DBPEDIA_LABELS_OWL = """#INSERT_DBPEDIA_LABELS_OWL
""" + PREFIX + """
DELETE
{
  ?bfLangId rdfs:label ?langLabel .
  ?bfLangId bf:label ?langLabel
}
INSERT
{?bfLangId bf:label ?langLabel}
WHERE
{

  	{
      ?bfLangId a bf:Language .
      ?bfLangId owl:sameAs ?p .
      FILTER (STRSTARTS(STR(?p),"http://dbpedia.org/resource/"))
      
     }
	SERVICE <http://DBpedia.org/sparql>
	{ 
      ?p rdfs:label ?langLabel. 
    }

}
"""

INSERT_DBPEDIA_LABELS = """#INSERT_DBPEDIA_LABELS
""" + PREFIX + """
DELETE
{
  ?bfLangId bf:label ?label
}
INSERT
{
  ?bfLangId bf:label ?label
}
WHERE 
{

  ?bfLangId a bf:Language .
  ?bfLangId dbo:wikiPageID ?wiki .

  SERVICE <http://DBpedia.org/sparql>
    { 
      ?dbPediaResource a dbo:Language .
      ?dbPediaResource dbo:wikiPageID  ?wiki .
      ?dbPediaResource rdfs:label ?label
    }
}"""
INSERT_DBPEDIA_LABELS_2 = """#INSERT_DBPEDIA_LABELS_2
""" + PREFIX + """
DELETE
{
  ?bfLangId bf:label ?label .
}
INSERT
{
  ?bfLangId bf:label ?label .
}
WHERE 
{

  OPTIONAL {
    ?bfLangId a bf:Language .
    ?bfLangId dbo:wikiPageID ?wiki .
    OPTIONAL {?bfLangId bf:label ?lab} .
    filter (!bound(?lab))
  }
  SERVICE <http://DBpedia.org/sparql>
    { 
      ?dbPediaResource dbo:wikiPageID  ?wiki .
      ?dbPediaResource rdfs:label ?label .
    }
}"""

INSERT_LABEL_VARIANTS_FROM_BF = """#INSERT_LABEL_VARIANTS_FROM_BF 
""" + PREFIX + """
DELETE
{
  ?langid	<http://www.loc.gov/mads/rdf/v1#hasVariant> ?oo .
} 
INSERT
{
  ?bfLangURI bf:labelVariant ?labelVariant .
}
WHERE
{
    <http://id.loc.gov/vocabulary/iso639-1> <http://www.loc.gov/mads/rdf/v1#hasTopMemberOfMADSScheme> ?langid.
  	?langid	<http://www.loc.gov/mads/rdf/v1#hasVariant> ?oo .
  	?oo <http://www.loc.gov/mads/rdf/v1#variantLabel> ?labelVariant .   
	  ?bfLangURI a	bf:Language .
    ?bfLangURI owl:sameAs ?langid .

}"""


INSERT_SOURCE_REFERENCE = """#INSERT_SOURCE_REFERENCE
""" + PREFIX + """
INSERT
{
?bfLangId bf:dataSource [
	bf:label [rdfs:label ?dbPediaResource];
	bf:summary [dbo:abstract ?dbPediaResource]
	]
}
WHERE
{

  ?bfLangId a bf:Language .
  ?bfLangId dbo:wikiPageID ?wiki .

  SERVICE <http://DBpedia.org/sparql>
    { 
      ?dbPediaResource a dbo:Language .
      ?dbPediaResource dbo:wikiPageID  ?wiki .
    }
}"""

REFORMAT_USEFOR_DATA = """#REFORMAT_USEFOR_DATA
""" + PREFIX + """
DELETE
{
  ?langid <http://www.loc.gov/mads/rdf/v1#useFor> ?ufObject .  
}
INSERT
{
  ?langid bf:useForMADS ?useFor .
}
WHERE
{
  ?langid a bf:Language .
  ?langid <http://www.loc.gov/mads/rdf/v1#useFor> ?ufObject .
  BIND (IF(ISBLANK(?ufObject), ?ufObject, "") AS ?bn) .
  ?bn <http://www.loc.gov/mads/rdf/v1#authoritativeLabel> ?useFor .
}
"""

REMOVE_LANGUAGES_TRIPLES = """#REMOVE_LANGUAGES_TRIPLES
""" + PREFIX + """
DELETE
{
  <http://id.loc.gov/vocabulary/languages> ?langP ?langO .  
}
WHERE
{
  <http://id.loc.gov/vocabulary/languages> ?langP ?langO .
}"""


REMOVE_REST_OF_ISO6391_EXTRA_DATA = """#REMOVE_REST_OF_ISO6391_EXTRA_DATA
""" + PREFIX + """
DELETE
{
 ?langid ?p ?o .
  <http://id.loc.gov/vocabulary/iso639-1/iso639-1_Language> ?pp ?oo 
}
WHERE
{
  ?langid <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSCollection>	<http://id.loc.gov/vocabulary/iso639-1/collection_PastPresentISO639-1Entries> .
  ?langid ?p ?o .
  <http://id.loc.gov/vocabulary/iso639-1/iso639-1_Language> ?pp ?oo .

}"""


TIE_ISO6391_ENTRIES_TO_BF_LANGUAGE_ENTRY = """#TIE_ISO6391_ENTRIES_TO_BF_LANGUAGE_ENTRY
""" + PREFIX + """
DELETE
{
  ?langid <http://www.loc.gov/mads/rdf/v1#hasExactExternalAuthority> ?langURI
}
INSERT
{
  ?langURI owl:sameAs ?langid
}
WHERE
{
  ?langid a  <http://id.loc.gov/vocabulary/iso639-1/iso639-1_Language> .
  ?langid <http://www.loc.gov/mads/rdf/v1#hasExactExternalAuthority> ?langURI .
  BIND(IF(STRSTARTS(STR(?langURI ),"http://id.loc.gov/vocabulary/languages/"),?langURI,"") AS ?bfLangURI) .
  FILTER (isURI(?bfLangURI))
}"""



UPDATE_BASE_LANGUAGE_ENTRIES = """#UPDATE_BASE_LANGUAGE_ENTRIES
""" + PREFIX + """
DELETE
{
  ?langid <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/vocabulary/languages> .
  ?langid a <http://id.loc.gov/vocabulary/languages/MARC_Language> .
  ?langid a <http://www.loc.gov/mads/rdf/v1#Authority> .
  ?langid a <http://www.loc.gov/mads/rdf/v1#Language> .
  ?langid a rdf:Resource .
  ?langid <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSCollection> <http://id.loc.gov/vocabulary/languages/collection_PastPresentLanguagesEntries> .
}
INSERT
{
  ?langid a bf:Language .
}
WHERE
{
  ?langid a <http://id.loc.gov/vocabulary/languages/MARC_Language> .
}"""

UPDATE_LABELS = """#UPDATE_LABELS
""" + PREFIX + """
DELETE
{
  ?langid <http://www.loc.gov/mads/rdf/v1#authoritativeLabel> ?label .
}
INSERT
{
  ?langid bf:shortLabel ?label .
}
WHERE
{
  ?langid a bf:Language .
  ?langid <http://www.loc.gov/mads/rdf/v1#authoritativeLabel> ?label  .
}"""

UPDATE_LANGUAGE_CODES = """#UPDATE_LANGUAGE_CODES
""" + PREFIX + """
DELETE
{
  ?langid <http://www.loc.gov/mads/rdf/v1#code> ?langIsoCode .
}
INSERT
{
  ?langid bfe:iso6392 ?langIsoCode .
}
WHERE
{
  ?langid a bf:Language .
  ?langid <http://www.loc.gov/mads/rdf/v1#code> ?langIsoCode  .
}"""


UPDATE_LOCSUBJECT_REFERENCE = """#UPDATE_LOCSUBJECT_REFERENCE
""" + PREFIX + """
DELETE
{
  ?langid <http://www.loc.gov/mads/rdf/v1#hasExactExternalAuthority> ?subjectId .
}
INSERT
{
  ?langid owl:sameAs ?subjectId .
  ?langid a bf:LocSubject .
}
WHERE
{
  ?langid a bf:Language .
  ?langid <http://www.loc.gov/mads/rdf/v1#hasExactExternalAuthority> ?subjectId .
}"""

CONFIRM_6392_LINKAGE_WITH_ISO6392_FILE = """#CONFIRM_6392_LINKAGE_WITH_ISO6392_FILE
""" + PREFIX + """
DELETE
{
  ?bfLangURI owl:sameAs ?6392id .
  ?6392id <http://www.loc.gov/mads/rdf/v1#hasExactExternalAuthority> ?bfLangURI
}

INSERT
{
  ?bfLangURI owl:sameAs ?6392id .
}
WHERE
{
?6392id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/vocabulary/iso639-2> .  
?6392id <http://www.loc.gov/mads/rdf/v1#hasExactExternalAuthority> ?langid .
  BIND(IF(STRSTARTS(STR(?langid),"http://id.loc.gov/vocabulary/languages/"),?langid,"") AS ?bfLangURI) .
  FILTER (isURI(?bfLangURI)) .
}"""

ADJUST_RDFTYPES_BASED_ON_ISO6392_FILE = """#ADJUST_RDFTYPES_BASED_ON_ISO6392_FILE
""" + PREFIX + """
DELETE
{

  ?6392id rdf:type	<http://www.loc.gov/mads/rdf/v1#Language> .
  ?6392id rdf:type	rdf:Resource .
  ?6392id rdf:type	<http://www.loc.gov/mads/rdf/v1#Language> .
  ?6392id rdf:type	<http://www.loc.gov/mads/rdf/v1#Authority> .
  ?6392id rdf:type	<http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language> .
  ?bfLangURI a <http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language> .
  ?bfLangURI a <http://id.loc.gov/vocabulary/iso639-2> .
}
INSERT
{
  ?bfLangURI a <http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language> .
  ?bfLangURI a <http://id.loc.gov/vocabulary/iso639-2> .
}
WHERE
{
  ?6392id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/vocabulary/iso639-2> .
  ?6392id a <http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language>.
  ?bfLangURI a	bf:Language .
  ?bfLangURI owl:sameAs ?6392id .
}"""

CONFIRM_LANGUAGE_6392_CODES_FROM_ISO6392_FILE = """#CONFIRM_LANGUAGE_6392_CODES_FROM_ISO6392_FILE
""" + PREFIX + """
DELETE
{
  ?6392id <http://www.loc.gov/mads/rdf/v1#code> ?langCode.
  ?bfLangURI bfe:iso6392 ?langCode.
}
INSERT
{
  ?bfLangURI a <http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language> .
  ?bfLangURI bfe:iso6392 ?langCode.
}
WHERE
{
  ?6392id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/vocabulary/iso639-2> .
  ?6392id <http://www.loc.gov/mads/rdf/v1#code> ?langCode.
  ?bfLangURI a	bf:Language .
  ?bfLangURI owl:sameAs ?6392id .
}"""

COPY_NOTES_FROM_ISO_6392 = """#COPY_NOTES_FROM_ISO_6392 
""" + PREFIX + """
DELETE
{
  ?langid	<http://www.loc.gov/mads/rdf/v1#historyNote> ?note .
  ?langid	<http://www.loc.gov/mads/rdf/v1#note> ?note .
  ?bfLangURI bf:note ?fnote .
}
INSERT
{
	?bfLangURI bf:note ?fnote
}
WHERE
{
   	{
      SELECT ?bfLangURI ?fnote ?note ?langid WHERE {
        <http://id.loc.gov/vocabulary/iso639-2> <http://www.loc.gov/mads/rdf/v1#hasTopMemberOfMADSScheme> ?langid.
        ?langid	<http://www.loc.gov/mads/rdf/v1#historyNote> ?note .
        BIND (CONCAT("ISO 639-2: ",?note) AS ?fnote) .
        ?bfLangURI a	bf:Language .
        ?bfLangURI owl:sameAs ?langid .}
    } UNION {
      SELECT ?bfLangURI ?fnote ?note ?langid WHERE {
        <http://id.loc.gov/vocabulary/iso639-2> <http://www.loc.gov/mads/rdf/v1#hasTopMemberOfMADSScheme> ?langid.
        ?langid	<http://www.loc.gov/mads/rdf/v1#note> ?note .
        BIND (CONCAT("ISO 639-2: ",?note) AS ?fnote) .
        ?bfLangURI a	bf:Language .
        ?bfLangURI owl:sameAs ?langid .}
    }
}"""

INSERT_LABEL_VARIANTS_FROM_ISO6392 = """#INSERT_LABEL_VARIANTS_FROM_ISO6392
""" + PREFIX + """
DELETE
{
  ?langid	<http://www.loc.gov/mads/rdf/v1#hasVariant> ?oo .
  ?bfLangURI bf:labelVariant ?labelVariant .
} 
INSERT
{
  ?bfLangURI bf:labelVariant ?labelVariant .
}
WHERE
{
    <http://id.loc.gov/vocabulary/iso639-2> <http://www.loc.gov/mads/rdf/v1#hasTopMemberOfMADSScheme> ?langid.
  	?langid	<http://www.loc.gov/mads/rdf/v1#hasVariant> ?oo .
  	?oo <http://www.loc.gov/mads/rdf/v1#variantLabel> ?labelVariant .   
	?bfLangURI a	bf:Language .
    ?bfLangURI owl:sameAs ?langid .

}"""

REMOVE_REST_OF_ISO6392_EXTRA_DATA =  """#REMOVE_REST_OF_ISO6392_EXTRA_DATA
""" + PREFIX + """
DELETE
{
 ?s ?p ?o .
}
WHERE
{
  ?s ?p ?o .
  FILTER (STRSTARTS(STR(?s), "http://id.loc.gov/vocabulary/iso639-2"))
}"""

CONFIRM_6395_LINKAGE_WITH_ISO6395_FILE = """#CONFIRM_6395_LINKAGE_WITH_ISO6395_FILE
""" + PREFIX + """
DELETE
{
  ?bfLangURI owl:sameAs ?6395id .
  ?6395id <http://www.loc.gov/mads/rdf/v1#hasExactExternalAuthority> ?bfLangURI
}

INSERT
{
  ?bfLangURI owl:sameAs ?6395id .
}
WHERE
{
  ?6395id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/vocabulary/iso639-5> .
  ?6395id <http://www.loc.gov/mads/rdf/v1#hasExactExternalAuthority> ?langid .
  BIND(IF(STRSTARTS(STR(?langid),"http://id.loc.gov/vocabulary/languages/"),?langid,"") AS ?bfLangURI) .
  FILTER (isURI(?bfLangURI)) .
}"""

CONSTRUCT_LANGUAGES_FOR_MISSING_ISO6395_LANGUAGES = """#CONSTRUCT_LANGUAGES_FOR_MISSING_ISO6395_LANGUAGES
""" + PREFIX + """
DELETE 
{
  ?newBfLangURI a <http://bibframe.org/vocab/Language>,
               <http://id.loc.gov/vocabulary/iso639-5/iso639-5_Language>,
               <http://id.loc.gov/vocabulary/iso639-5>;
             owl:sameAs ?6395id;
             bfe:iso6395 ?langCode .
  ?6395id a <http://id.loc.gov/vocabulary/iso639-5/iso639-5_Language>.
  ?6395id <http://www.loc.gov/mads/rdf/v1#code> ?langCode .
}

INSERT 
{
  ?newBfLangURI a <http://bibframe.org/vocab/Language>,
               <http://id.loc.gov/vocabulary/iso639-5/iso639-5_Language>,
               <http://id.loc.gov/vocabulary/iso639-5>;
             owl:sameAs ?6395id;
             bfe:iso6395 ?langCode .
}

WHERE
{
  ?6395id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/vocabulary/iso639-5> .
  OPTIONAL {?bfLangURI a	bf:Language .
            ?bfLangURI owl:sameAs ?6395id .}
  FILTER (!bound(?bfLangURI)).
  ?6395id <http://www.loc.gov/mads/rdf/v1#code> ?langCode .
  BIND (URI(CONCAT("http://id.loc.gov/vocabulary/languages/",?langCode)) as ?newBfLangURI)
  
}"""

INSERT_SHORTLABELS_FOR_MISSING_ISO6395_LANGUAGES = """#INSERT_SHORTLABELS_FOR_MISSING_ISO6395_LANGUAGES
""" + PREFIX + """
DELETE
{
  ?bfLangURI bf:label ?label .
  ?6395id <http://www.loc.gov/mads/rdf/v1#authoritativeLabel> ?label
}

INSERT
{
  ?bfLangURI bf:label ?label .
}

WHERE
{
  ?6395id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/vocabulary/iso639-5> .
  ?bfLangURI a	bf:Language .
  ?bfLangURI owl:sameAs ?6395id .
  OPTIONAL {?bfLangURI bf:shortLabel ?bfLabel .}
  FILTER (!bound(?bfLabel)).
  ?6395id <http://www.loc.gov/mads/rdf/v1#authoritativeLabel> ?label.
}"""



COPY_NOTES_FROM_ISO_6395 = """#COPY_NOTES_FROM_ISO_6395
""" + PREFIX + """
DELETE
{
  ?6395id	<http://www.loc.gov/mads/rdf/v1#historyNote> ?note .
  ?6395id	<http://www.loc.gov/mads/rdf/v1#note> ?note .
  ?6395id	<http://www.loc.gov/mads/rdf/v1#scopeNote> ?note .
  ?bfLangURI bf:note ?fnote .
}
INSERT
{
	?bfLangURI bf:note ?fnote
}
WHERE
{
   	{
      SELECT ?bfLangURI ?fnote ?note ?6395id WHERE {
        ?6395id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/vocabulary/iso639-5> .
        ?6395id	<http://www.loc.gov/mads/rdf/v1#historyNote> ?note .
        BIND (CONCAT("ISO 639-5: ",?note) AS ?fnote) .
        ?bfLangURI a	bf:Language .
        ?bfLangURI owl:sameAs ?6395id .}
    } UNION {
      SELECT ?bfLangURI ?fnote ?note ?6395id WHERE {
        ?6395id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/vocabulary/iso639-5> .
        ?6395id	<http://www.loc.gov/mads/rdf/v1#note> ?note .
        BIND (CONCAT("ISO 639-5: ",?note) AS ?fnote) .
        ?bfLangURI a	bf:Language .
        ?bfLangURI owl:sameAs ?6395id .}
    } UNION {
      SELECT ?bfLangURI ?fnote ?note ?6395id WHERE {
        ?6395id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/vocabulary/iso639-5> .
        ?6395id	<http://www.loc.gov/mads/rdf/v1#scopeNote> ?note .
        BIND (?note AS ?fnote) .
        ?bfLangURI a	bf:Language .
        ?bfLangURI owl:sameAs ?6395id .}
    }
}"""

INSERT_LABEL_VARIANTS_FROM_ISO6395 = """#INSERT_LABEL_VARIANTS_FROM_ISO6395
""" + PREFIX + """
DELETE
{
  ?6395id	<http://www.loc.gov/mads/rdf/v1#hasVariant> ?oo .
  ?bfLangURI bf:labelVariant ?labelVariant .
} 
INSERT
{
  ?bfLangURI bf:labelVariant ?labelVariant .
}
WHERE
{
    ?6395id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/vocabulary/iso639-5> .
  	?6395id	<http://www.loc.gov/mads/rdf/v1#hasVariant> ?oo .
  	?oo <http://www.loc.gov/mads/rdf/v1#variantLabel> ?labelVariant .   
	?bfLangURI a	bf:Language .
    ?bfLangURI owl:sameAs ?6395id .

}"""

CONFIRM_LANGUAGE_6395_CODES_FROM_ISO6395_FILE = """#CONFIRM_LANGUAGE_6395_CODES_FROM_ISO6395_FILE
""" + PREFIX + """
DELETE
{
  ?6395id <http://www.loc.gov/mads/rdf/v1#code> ?langCode.
  ?bfLangURI bfe:iso6395 ?langCode.
}
INSERT
{
  ?bfLangURI a <http://id.loc.gov/vocabulary/iso639-5/iso639-5_Language> .
  ?bfLangURI bfe:iso6395 ?langCode.
}
WHERE
{
  ?6395id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/vocabulary/iso639-5> .
  ?6395id <http://www.loc.gov/mads/rdf/v1#code> ?langCode.
  ?bfLangURI a	bf:Language .
  ?bfLangURI owl:sameAs ?6395id .
}"""

ADJUST_RDFTYPES_BASED_ON_ISO6395_FILE = """#ADJUST_RDFTYPES_BASED_ON_ISO6395_FILE
""" + PREFIX + """
DELETE
{

  ?6395id rdf:type	<http://www.loc.gov/mads/rdf/v1#Language> .
  ?6395id rdf:type	rdf:Resource .
  ?6395id rdf:type	<http://www.loc.gov/mads/rdf/v1#Language> .
  ?6395id rdf:type	<http://www.loc.gov/mads/rdf/v1#Authority> .
  ?6395id rdf:type	<http://id.loc.gov/vocabulary/iso639-5/iso639-5_Language> .
  ?6395id <http://www.loc.gov/mads/rdf/v1#isTopMemberOfMADSScheme> <http://id.loc.gov/vocabulary/iso639-5> .
  ?bfLangURI a <http://id.loc.gov/vocabulary/iso639-5/iso639-5_Language> .
  ?bfLangURI a <http://id.loc.gov/vocabulary/iso639-5> .
}
INSERT
{
  ?bfLangURI a <http://id.loc.gov/vocabulary/iso639-5/iso639-5_Language> .
  ?bfLangURI a <http://id.loc.gov/vocabulary/iso639-5> .
}
WHERE
{
  ?6395id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/vocabulary/iso639-5> .
  ?bfLangURI a	bf:Language .
  ?bfLangURI owl:sameAs ?6395id .
}"""

ADJUST_RDFTYPES_BASED_ON_COLLECTIONS_IN_ISO6395_FILE = """#ADJUST_RDFTYPES_BASED_ON_COLLECTIONS_IN_ISO6395_FILE
""" + PREFIX + """
DELETE
{
  ?6395id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSCollection> ?rdfType .
  ?bfLangURI a ?rdfType .
}
INSERT
{
  ?bfLangURI a ?rdfType .
}
WHERE
{
  ?6395id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/vocabulary/iso639-5> .
  ?6395id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSCollection> ?rdfType .
  ?bfLangURI a	bf:Language .
  ?bfLangURI owl:sameAs ?6395id .
}"""

ADJUST_ADD_SKOS_BROADER_RELATIONSHIPS_FROM_ISO6395 ="""#ADJUST_ADD_SKOS_BROADER_RELATIONSHIPS_FROM_ISO6395
""" + PREFIX + """
DELETE
{
  ?6395id <http://www.loc.gov/mads/rdf/v1#hasBroaderAuthority> ?broader
}
INSERT
{
  ?bfLangURI skos:broader ?rdfType .
}
WHERE
{
  ?6395id <http://www.loc.gov/mads/rdf/v1#isMemberOfMADSScheme>	<http://id.loc.gov/vocabulary/iso639-5> .
  ?6395id <http://www.loc.gov/mads/rdf/v1#hasBroaderAuthority> ?broader .
  ?bfLangURI a	bf:Language .
  ?bfLangURI owl:sameAs ?6395id .
}"""

REMOVE_REST_OF_ISO6395_EXTRA_DATA = """#REMOVE_REST_OF_ISO6395_EXTRA_DATA
""" + PREFIX + """
DELETE
{
 ?s ?p ?o .
}
WHERE
{
  ?s ?p ?o .
  FILTER (STRSTARTS(STR(?s), "http://id.loc.gov/vocabulary/iso639-5"))
}"""

CLEAN_MISC_MADS_TRIPLES = """#CLEAN_MISC_MADS_TRIPLES
""" + PREFIX + """
DELETE
{
  <http://id.loc.gov/vocabulary/languages/collection_PastPresentLanguagesEntries> ?p ?o . 
  <http://id.loc.gov/vocabulary/iso639-1/collection_PastPresentISO639-1Entries> ?pp ?oo .
}

WHERE
{
  <http://id.loc.gov/vocabulary/languages/collection_PastPresentLanguagesEntries> ?p ?o . 
  <http://id.loc.gov/vocabulary/iso639-1/collection_PastPresentISO639-1Entries> ?pp ?oo .
}"""
ESTABLISH_DBPEDIA_LINKAGE_VIA_ISO6392 = """#ESTABLISH_DBPEDIA_LINKAGE_VIA_ISO6392
""" + PREFIX + """
DELETE
{
  ?langid owl:sameAs ?dbPediaResource .
  ?langid dbo:wikiPageID ?wikiPageID .
}
INSERT
{
  ?langid owl:sameAs ?dbPediaResource .
  ?langid dbo:wikiPageID ?wikiPageID .
}
WHERE
{
  ?langid a	bf:Language .
  ?langid bfe:iso6392 ?langIsoCode .
  SERVICE <http://DBpedia.org/sparql>
    { 
      ?dbPediaResource dbo:iso6392Code ?langIsoCode .
      ?dbPediaResource dbo:wikiPageID ?wikiPageID .
    } 
}
"""
ESTABLISH_DBPEDIA_LINKAGE_VIA_ISO6393 = """#ESTABLISH_DBPEDIA_LINKAGE_VIA_ISO6393
""" + PREFIX + """
DELETE
{
  ?bfLangId owl:sameAs ?dbPediaResource .
  ?bfLangId dbo:wikiPageID ?wikiPageID .
}
INSERT
{
  ?bfLangId owl:sameAs ?dbPediaResource .
  ?bfLangId dbo:wikiPageID ?wikiPageID .
}
WHERE

{
  ?bfLangId a bf:Language .
  OPTIONAL
  	{
      ?bfLangId owl:sameAs ?p .
  		BIND (IF(STRSTARTS(STR(?p),"http://dbpedia.org/resource/"),?p,"") as ?dbpObject) .
  		?bfLangId owl:sameAs ?dbpObject .
      }
	FILTER (!bound(?dbpObject)) .
  ?bfLangId bfe:iso6392 ?code .
   SERVICE <http://DBpedia.org/sparql>
    { 
      ?dbPediaResource dbo:iso6393Code ?code .
      ?dbPediaResource dbo:wikiPageID ?wikiPageID .
    } 
}
"""

GENERATE_TEMP_ISO_EN_TAGS_FOR_DBPEDIA_LINKAGE = """#GENERATE_TEMP_ISO_EN_TAGS_FOR_DBPEDIA_LINKAGE
""" + PREFIX + """
INSERT
	{?bfLangId bf:temp ?enCode}
WHERE

{
  ?bfLangId a bf:Language .
  OPTIONAL
  	{
      ?bfLangId owl:sameAs ?p .
  		BIND (IF(STRSTARTS(STR(?p),"http://dbpedia.org/resource/"),?p,"") as ?dbpObject) .
  		?bfLangId owl:sameAs ?dbpObject .
      }
	FILTER (!bound(?dbpObject)) .
  	?bfLangId bfe:iso6395 ?code .
  	BIND (STRLANG(STR(?code),"en") as ?enCode) .
  
}"""

LINK_TEMP_ISO_EN_TAGS_FOR_DBPEDIA = """#LINK_TEMP_ISO_EN_TAGS_FOR_DBPEDIA
""" + PREFIX + """
INSERT
	{
	  ?bfLangId owl:sameAs ?dbPediaResource .
	  ?bfLangId dbo:wikiPageID ?wikiPageID
	}
WHERE
{
  ?bfLangId a bf:Language .
  ?bfLangId bf:temp ?enCode .
   
  SERVICE <http://DBpedia.org/sparql> 
  { 
    ?dbPediaResource <http://dbpedia.org/property/iso> ?enCode . 
    ?dbPediaResource dbo:wikiPageID ?wikiPageID .
  }
  
}"""

ESTABLISH_DBPEDIA_LINKAGE_VIA_ISO6391 = """#ESTABLISH_DBPEDIA_LINKAGE_VIA_ISO6391
""" + PREFIX + """
DELETE
{
  ?bfLangId owl:sameAs ?dbPediaResource .
  ?bfLangId dbo:wikiPageID ?wikiPageID .
}
INSERT
{
  ?bfLangId owl:sameAs ?dbPediaResource .
  ?bfLangId dbo:wikiPageID ?wikiPageID .
}
WHERE

{
  ?bfLangId a bf:Language .
  OPTIONAL
  	{
      ?bfLangId owl:sameAs ?p .
  		BIND (IF(STRSTARTS(STR(?p),"http://dbpedia.org/resource/"),?p,"") as ?dbpObject) .
  		?bfLangId owl:sameAs ?dbpObject .
      }
	FILTER (!bound(?dbpObject)) .
  ?bfLangId bfe:iso6391 ?code .
   SERVICE <http://DBpedia.org/sparql>
    { 
      ?dbPediaResource dbo:iso6391Code ?code .
      ?dbPediaResource dbo:wikiPageID ?wikiPageID .
    } 
}
"""

GENERATE_TEMP_REDIRECT_TAGS_FOR_DBPEDIA_LINKAGE = """#GENERATE_TEMP_REDIRECT_TAGS_FOR_DBPEDIA_LINKAGE 
""" + PREFIX + """
DELETE {?bfLangId bf:tempR ?dbRedirect}
INSERT {?bfLangId bf:tempR ?dbRedirect}
WHERE

{
  ?bfLangId a bf:Language .
  OPTIONAL
  	{
      ?bfLangId owl:sameAs ?p .
  		BIND (IF(STRSTARTS(STR(?p),"http://dbpedia.org/resource/"),?p,"") as ?dbpObject) .
  		?bfLangId owl:sameAs ?dbpObject .
    }
	FILTER (!bound(?dbpObject)) .
	OPTIONAL {?bfLangId bfe:iso6395 ?code .}
  OPTIONAL {?bfLangId bfe:iso6392 ?code .}
  BIND (URI(CONCAT("http://dbpedia.org/resource/ISO_639:",?code)) AS ?dbRedirect) .
}"""

INSERT_DBPEDIA_REDIRECT_TAGS = """#INSERT_DBPEDIA_REDIRECT_TAGS
""" + PREFIX + """
INSERT
	{
	  ?dbr bf:tempRR ?dbpResource .
	  ?dbr dbo:wikiPageID ?wikiPageID .
	}
WHERE
{
  
  SERVICE <http://DBpedia.org/sparql> {	
    ?dbr <http://dbpedia.org/ontology/wikiPageRedirects> ?dbpResource .
    FILTER (STRSTARTS(STR(?dbr),"http://dbpedia.org/resource/ISO_639")) .
    ?dbpResource dbo:wikiPageID ?wikiPageID .
  }
  
}"""

USE_DBPEDIA_REDIRECT_TAGS_LINKAGE = """#USE_DBPEDIA_REDIRECT_TAGS_LINKAGE
""" + PREFIX + """
DELETE
	{
	  ?bfLangId owl:sameAs ?dbr .
	  ?bfLangId dbo:wikiPageID ?wikiPageID .
	}
INSERT
	{
	  ?bfLangId owl:sameAs ?dbr .
	  ?bfLangId dbo:wikiPageID ?wikiPageID .
	}
WHERE
{
  ?bfLangId a bf:Language .
  ?bfLangId bf:tempR ?dbRedirect .
  ?dbRedirect bf:tempRR ?dbr.
  ?dbRedirect dbo:wikiPageID ?wikiPageID .
  FILTER (?dbr!=<http://dbpedia.org/resource/ISO_639-3>)
}"""

DELETE_TEMP_TRIPLES_1 = """#DELETE_TEMP_TRIPLES_1
""" + PREFIX + """
DELETE
{
  ?s bf:temp ?o .
}
  
WHERE

{
  ?s bf:temp ?o .
}"""

DELETE_TEMP_TRIPLES_2 = """#DELETE_TEMP_TRIPLES_2
""" + PREFIX + """
DELETE
{
  ?s bf:tempR ?o .
}
  
WHERE

{
  ?s bf:tempR ?o .
}"""
DELETE_TEMP_TRIPLES_3 = """#DELETE_TEMP_TRIPLES_3
""" + PREFIX + """
DELETE
{
  ?s bf:tempRR ?o .
  ?s dbo:wikiPageID ?oo .
}
  
WHERE

{
  ?s bf:tempRR ?o .
  ?s dbo:wikiPageID ?oo .
}"""

ADD_OWLSAMEAS_TAG_FOR_LANG_URI = """#ADD_OWLSAMEAS_TAG_FOR_LANG_URI
""" + PREFIX + """
DELETE
{
  ?bfLangId owl:sameAs ?bfLangId
}
INSERT 
{
  ?bfLangId owl:sameAs ?bfLangId
}
WHERE
{
  ?bfLangId a bf:Language .
  OPTIONAL {?id2 owl:sameAs ?bfLangId.} .
  FILTER (!bound(?id2))
}"""
CHANGE_BASE_URI = """#CHANGE_BASE_URI
""" + PREFIX + """
DELETE
{ 
  ?bfLangId ?p ?o
}
INSERT
{
  ?fedoraURI ?p ?o
}
WHERE
{
  ?bfLangId a bf:Language .
  BIND (URI(REPLACE(STR(?bfLangId),"http://id.loc.gov/vocabulary/languages/","http://knowledgelinks.io/ns/bibcat/")) AS ?fedoraURI)
  ?bfLangId ?p ?o 
}"""

workflow = [
    UPDATE_BASE_LANGUAGE_ENTRIES,
    DELETE_MADS_ADMIN_METADATA,
    UPDATE_LOCSUBJECT_REFERENCE,
    UPDATE_LABELS,
    UPDATE_LANGUAGE_CODES,
    DELETE_LANGUAGE_NOTES,   
    REMOVE_LANGUAGES_TRIPLES,   
    REFORMAT_USEFOR_DATA,
    TIE_ISO6391_ENTRIES_TO_BF_LANGUAGE_ENTRY,   
    ADD_ISO6391_TO_RDF_TYPE_AND_DELETE_EXTRA_FIELDS,
    ADD_ISO6392_LINKAGE_FROM_ISO6391_RDF_FILE,
    COPY_NOTES_FROM_ISO_6391,
    REMOVE_REST_OF_ISO6391_EXTRA_DATA,
    CONFIRM_6392_LINKAGE_WITH_ISO6392_FILE,
    ADJUST_RDFTYPES_BASED_ON_ISO6392_FILE,
    CONFIRM_LANGUAGE_6392_CODES_FROM_ISO6392_FILE,
    COPY_NOTES_FROM_ISO_6392,
    INSERT_LABEL_VARIANTS_FROM_ISO6392,
    REMOVE_REST_OF_ISO6392_EXTRA_DATA,
    CONFIRM_6395_LINKAGE_WITH_ISO6395_FILE,
    CONSTRUCT_LANGUAGES_FOR_MISSING_ISO6395_LANGUAGES,
    INSERT_SHORTLABELS_FOR_MISSING_ISO6395_LANGUAGES,
    COPY_NOTES_FROM_ISO_6395,
    INSERT_LABEL_VARIANTS_FROM_ISO6395,
    CONFIRM_LANGUAGE_6395_CODES_FROM_ISO6395_FILE,
    ADJUST_RDFTYPES_BASED_ON_ISO6395_FILE,
    ADJUST_RDFTYPES_BASED_ON_COLLECTIONS_IN_ISO6395_FILE,
    ADJUST_ADD_SKOS_BROADER_RELATIONSHIPS_FROM_ISO6395,
    REMOVE_REST_OF_ISO6395_EXTRA_DATA,
    CLEAN_MISC_MADS_TRIPLES,
    ESTABLISH_DBPEDIA_LINKAGE_VIA_ISO6392,
    ESTABLISH_DBPEDIA_LINKAGE_VIA_ISO6393,
    GENERATE_TEMP_ISO_EN_TAGS_FOR_DBPEDIA_LINKAGE,
    LINK_TEMP_ISO_EN_TAGS_FOR_DBPEDIA,
    ESTABLISH_DBPEDIA_LINKAGE_VIA_ISO6391,
    GENERATE_TEMP_REDIRECT_TAGS_FOR_DBPEDIA_LINKAGE,
    INSERT_DBPEDIA_REDIRECT_TAGS,
    USE_DBPEDIA_REDIRECT_TAGS_LINKAGE,
    DELETE_TEMP_TRIPLES_1,
    DELETE_TEMP_TRIPLES_2,
    DELETE_TEMP_TRIPLES_3,
    INSERT_DBPEDIA_LABELS_OWL, 
    INSERT_DBPEDIA_ABSTRACTS_OWL,
    INSERT_SOURCE_REFERENCE,
    ADD_OWLSAMEAS_TAG_FOR_LANG_URI,
    CHANGE_BASE_URI,
    CLEAN_UP_ORPHAN_BLANK_NODES,
    CLEAN_UP_ORPHAN_BLANK_NODES,
    CLEAN_UP_ORPHAN_BLANK_NODES, 
]
