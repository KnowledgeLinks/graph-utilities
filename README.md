# RDF Graph Utilities
This Python module is a collection of RDF manipulation and filtering tools
initially targeted at BIBFRAME vocabulary work.

## To use
Run the following command from this directory to run all of the SPARQL statements
against a triplestore SPARQL endpoint using REST.

`python3 run.py languages`

Run the following command to pull a graph

`python run.py graph --graphargs "{see below}"`
    
    default graphargs = "{'pulltype':'all','sparqlselect':
                         "?s1 a bf:Language','format':'application/x-turtle',
                         'filename':'bibcatlanguages.ttl'}"

**** use json object notation; both object and value must have quotes

`'pulltype': 'all'--write triple statement in 'sparqlselect'`
            `'resource'--write resourceURI in the 'resourceURI' variable`
                        
`'resourceuri':  used with 'pulltype'=resource -- write resourceURI as a string WITHOUT <>`
         
`'sparqlselect':  used with 'pulltype'=all -- write the sparql triple to statment to select the `
`                 the resources that you want. variable ?s1 must contain the list of resource URIs`
`                 example: ?s1 rdf:type bf:Language   --will return all the language graphs`
         
`'format':  Use the header value of the rest API of the desired outputtype` 
`            Example: for turtle 'application/x-turtle'`
                 
`'filename': 'default' will use the sparql header provided filename.`
             `otherwise specify your own value`
