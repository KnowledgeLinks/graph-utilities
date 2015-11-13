__author__ = "Mike Stabile"

from . import PREFIX


ADD_ISO6391_TO_RDF_TYPE_AND_DELETE_EXTRA_FIELDS = PREFIX + """
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
  ?bfLangURI bf:iso639_1 ?langCode .
}
WHERE
{
  ?bfLangURI a	bf:Language .
  ?langid a  <http://id.loc.gov/vocabulary/iso639-1/iso639-1_Language> .
  ?bfLangURI owl:sameAs ?langid .
  ?langid <http://www.loc.gov/mads/rdf/v1#hasExactExternalAuthority> ?langURI .
  ?langid <http://www.loc.gov/mads/rdf/v1#code> ?langCode .
}"""

ADD_ISO6392_LINKAGE_FROM_ISO6391_RDF_FILE = PREFIX + """
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

COPY_NOTES_FROM_ISO_6391 = PREFIX + """
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


DELETE_LANGUAGE_NOTES = PREFIX + """{}
DELETE
{
  ?langid <http://www.loc.gov/mads/rdf/v1#editorialNote> ?note .
}
WHERE
{
  ?langid a bf:Language .
  ?langid <http://www.loc.gov/mads/rdf/v1#editorialNote> ?note .
}"""


DELETE_MADS_ADMIN_METADATA = PREFIX + """
DELETE
{
  ?langid <http://www.loc.gov/mads/rdf/v1#adminMetadata> ?adminObject .
}
WHERE
{
  ?langid a bf:Language .
  ?langid <http://www.loc.gov/mads/rdf/v1#adminMetadata> ?adminObject .
}"""

INSERT_DBPEDIA_ABSTRACTS = PREFIX + """
INSERT
{
  ?langid bf:summary ?summary .
}
WHERE
{
  ?langid bf:iso639_2 ?langIsoCode .
  SERVICE <http://DBpedia.org/sparql>
    { 
      ?dbPediaResource dbpo:iso6392Code ?langIsoCode .
      ?dbPediaResource dbpo:abstract ?summary .
    } 
}
"""

INSERT_DBPEDIA_LABELS = PREFIX + """
INSERT
{
  ?langid bf:label ?langLabel .
}
WHERE
{
  ?langid bf:iso639_2 ?langIsoCode .
  SERVICE <http://DBpedia.org/sparql>
    { 
      ?dbPediaResource dbpo:iso6392Code ?langIsoCode .
      ?dbPediaResource rdfs:label ?langLabel .
    } 
}"""

INSERT_LABEL_VARIANTS_FROM_BF = PREFIX + """
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


INSERT_SOURCE_REFERENCE_AND_OWL_SAMEAS = PREFIX + """
INSERT
{
?langid owl:sameAs ?dbPediaResource .  
?langid bf:dataSource [
	bf:label [rdfs:label ?dbPediaResource];
	bf:summary [dbpo:abstract ?dbPediaResource]
	]
}
WHERE
{
  ?langid bf:iso639_2 ?langIsoCode .
  SERVICE <http://DBpedia.org/sparql>
    { 
      ?dbPediaResource dbpo:iso6392Code ?langIsoCode .
    } 
}"""

REFORMAT_USEFOR_DATA = PREFIX + """
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

REMOVE_LANGUAGES_TRIPLES = PREFIX + """
DELETE
{
  <http://id.loc.gov/vocabulary/languages> ?langP ?langO .  
}
WHERE
{
  <http://id.loc.gov/vocabulary/languages> ?langP ?langO .
}"""


REMOVE_REST_OF_ISO6391_EXTRA_DATA = PREFIX + """
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


TIE_ISO6391_ENTRIES_TO_BF_LANGUAGE_ENTRY = PREFIX + """
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



UPDATE_BASE_LANGUAGE_ENTRIES = PREFIX + """
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

UPDATE_LABELS = PREFIX + """
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

UPDATE_LANGUAGE_CODES = PREFIX + """
DELETE
{
  ?langid <http://www.loc.gov/mads/rdf/v1#code> ?langIsoCode .
}
INSERT
{
  ?langid bf:iso639_2 ?langIsoCode .
}
WHERE
{
  ?langid a bf:Language .
  ?langid <http://www.loc.gov/mads/rdf/v1#code> ?langIsoCode  .
}"""


UPDATE_LOCSUBJECT_REFERENCE = PREFIX + """
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

workflow = [
    UPDATE_BASE_LANGUAGE_ENTRIES,
    DELETE_MADS_ADMIN_METADATA,
    UPDATE_LOCSUBJECT_REFERENCE,
    UPDATE_LABELS,
    UPDATE_LANGUAGE_CODES,
    DELETE_LANGUAGE_NOTES,   
    REMOVE_LANGUAGES_TRIPLES,   

    REFORMAT_USEFOR_DATA,
    INSERT_SOURCE_REFERENCE_AND_OWL_SAMEAS,
    TIE_ISO6391_ENTRIES_TO_BF_LANGUAGE_ENTRY,   
    ADD_ISO6391_TO_RDF_TYPE_AND_DELETE_EXTRA_FIELDS,
    ADD_ISO6392_LINKAGE_FROM_ISO6391_RDF_FILE,
    COPY_NOTES_FROM_ISO_6391,
    REMOVE_REST_OF_ISO6391_EXTRA_DATA
]
#    INSERT_DBPEDIA_LABELS,   
#    INSERT_DBPEDIA_ABSTRACTS,