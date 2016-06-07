from abc import ABCMeta
from QuitDiffSerializer import QuitDiffSerializer
from rdflib import URIRef, BNode, Literal, Namespace, Graph, ConjunctiveGraph
from rdflib.namespace import RDF
import uuid


class EccrevDiff(metaclass=ABCMeta):
    def serialize(self, add, delete):


        diff = Namespace("urn:diff:" + str(uuid.uuid1()) + ":")
        eccrev = Namespace("https://vocab.eccenca.com/revision/")
        #@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        g = ConjunctiveGraph()
        g.add( (diff.diff, RDF.type, eccrev.Commit) )


        graphUris = set(delete.keys()) | set(add.keys())

        for graphUri in graphUris:
            if (graphUri in delete.keys() and len(delete[graphUri]) > 0) or (graphUri in add.keys() and len(add[graphUri]) > 0):
                revId = "rev-" + str(uuid.uuid1())
                graphTerm = diff.term(revId)
                g.add( (diff.diff, eccrev.hasRevision, graphTerm) )
                g.add( (graphTerm, RDF.type, eccrev.Revision) )
                g.add( (graphTerm, eccrev.hasRevisionGraph, graphUri) )
                if graphUri in delete.keys() and len(delete[graphUri]) > 0:
                    deleteGraphName = diff.term(revId + ":delete")
                    g.add( (graphTerm, eccrev.deltaDelete, deleteGraphName) )
                    for triple in delete[graphUri]:
                        g.add(triple + (deleteGraphName,))
                if graphUri in add.keys() and len(add[graphUri]) > 0:
                    insertGraphName = diff.term(revId + ":insert")
                    g.add( (graphTerm, eccrev.deltaInsert, insertGraphName) )
                    for triple in add[graphUri]:
                        g.add(triple + (insertGraphName,))

        return g.serialize(format="trig").decode("utf-8")

EccrevDiff.register(QuitDiffSerializer)
