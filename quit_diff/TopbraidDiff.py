from abc import ABCMeta
from QuitDiffSerializer import QuitDiffSerializer
from rdflib import BNode, Namespace, ConjunctiveGraph
from rdflib.namespace import RDF, OWL, NamespaceManager
import uuid


class TopbraidDiff(metaclass=ABCMeta):
    def serialize(self, add, delete):

        """
        Serialize RDF deltas using topbraids diff ontology: http://topbraid.org/diff

        more info:
        * https://composing-the-semantic-web.blogspot.de/2009/07/spin-diff-rule-based-comparison-of-rdf.html
        * https://www.w3.org/2001/sw/wiki/How_to_diff_RDF
        """

        diff = Namespace("http://topbraid.org/diff#")

        g = ConjunctiveGraph()

        namespace_manager = NamespaceManager(g)
        namespace_manager.bind('diff', diff, override=False)
        namespace_manager.bind('owl', OWL, override=False)

        graphUris = set(delete.keys()) | set(add.keys())

        for graphUri in graphUris:
            if (graphUri in delete.keys() and len(delete[graphUri]) > 0) or (graphUri in add.keys() and len(add[graphUri]) > 0):
                changeset = Namespace("urn:diff:" + str(uuid.uuid1()))
                graphTerm = changeset.term("")
                if str(graphUri) != 'default':
                    g.add( (graphTerm, OWL.imports, graphUri, graphTerm) )
                g.add( (graphTerm, RDF.type, OWL.Ontology, graphTerm) )
                g.add( (graphTerm, OWL.imports, diff.term(""), graphTerm) )
                if graphUri in delete.keys() and len(delete[graphUri]) > 0:
                    i = 0
                    for triple in delete[graphUri]:
                        deleteStatementName = BNode()
                        g.add( (deleteStatementName, RDF.type, diff.DeletedTripleDiff, graphTerm) )
                        g.add( (deleteStatementName, RDF.subject, triple[0], graphTerm) )
                        g.add( (deleteStatementName, RDF.predicate, triple[1], graphTerm) )
                        g.add( (deleteStatementName, RDF.object, triple[2], graphTerm) )
                        i += 1
                if graphUri in add.keys() and len(add[graphUri]) > 0:
                    i = 0
                    for triple in add[graphUri]:
                        insertGraphName = BNode()
                        g.add( (insertGraphName, RDF.type, diff.AddedTripleDiff, graphTerm) )
                        g.add( (insertGraphName, RDF.subject, triple[0], graphTerm) )
                        g.add( (insertGraphName, RDF.predicate, triple[1], graphTerm) )
                        g.add( (insertGraphName, RDF.object, triple[2], graphTerm) )
                        i += 1

        return g.serialize(format="trig").decode("utf-8")

TopbraidDiff.register(QuitDiffSerializer)
