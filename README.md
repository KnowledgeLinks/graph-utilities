# RDF Graph Utilities
This Python module is a collection of RDF manipulation and filtering tools
initially targeted at BIBFRAME vocabulary work.

## To use
Run the following command from this directory to run all of the SPARQL statements
against a triplestore SPARQL endpoint using REST.

`python3 run.py languages`

Run the following command to pull the graph of a specific resourse and save it to a ttl file

`python run.py graph --graphuri "resourceURI"`
