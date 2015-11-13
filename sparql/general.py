__author__ = "Mike Stabile"

from . import PREFIX

CLEAN_UP_ORPHAN_BLANK_NODES = """#CLEAN_UP_ORPHAN_BLANK_NODES
""" + PREFIX +"""
DELETE
{
 ?bn ?p ?o
}
WHERE
{
  ?s ?p ?o .
  bind (if(isBLANK(?s),?s,"") AS ?bn) .
  ?bn ?p ?o .
  OPTIONAL {?parentBn ?pp ?bn} .
  FILTER (!bound(?parentBn))
}"""

