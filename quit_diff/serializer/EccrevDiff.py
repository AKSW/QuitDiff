from abc import ABCMeta
from ..QuitDiff import QuitDiffSerializer
from rdflib import Namespace, ConjunctiveGraph
from rdflib.namespace import RDF, NamespaceManager
import uuid


class EccrevDiff(metaclass=ABCMeta):
    def serialize(self, add, delete):


        commit = Namespace("urn:commit:" + str(uuid.uuid1()) + ":")
        eccrev = Namespace("https://vocab.eccenca.com/revision/")
        #@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        g = ConjunctiveGraph()
        namespace_manager = NamespaceManager(g)
        namespace_manager.bind('eccrev', eccrev, override=False)

        g.add( (commit.term(""), RDF.type, eccrev.Commit) )

        graphUris = set(delete.keys()) | set(add.keys())

        for graphUri in graphUris:
            if (graphUri in delete.keys() and len(delete[graphUri]) > 0) or (graphUri in add.keys() and len(add[graphUri]) > 0):
                revision = Namespace("urn:revision:" + str(uuid.uuid1()) + ":")
                g.add( (commit.term(""), eccrev.hasRevision, revision.term("")) )
                g.add( (revision.term(""), RDF.type, eccrev.Revision) )
                if str(graphUri) != 'default':
                    g.add( (revision.term(""), eccrev.hasRevisionGraph, graphUri) )
                if graphUri in delete.keys() and len(delete[graphUri]) > 0:
                    deleteGraphName = revision.term(":delete")
                    g.add( (revision.term(""), eccrev.deltaDelete, deleteGraphName) )
                    for triple in delete[graphUri]:
                        g.add(triple + (deleteGraphName,))
                if graphUri in add.keys() and len(add[graphUri]) > 0:
                    insertGraphName = revision.term(":insert")
                    g.add( (revision.term(""), eccrev.deltaInsert, insertGraphName) )
                    for triple in add[graphUri]:
                        g.add(triple + (insertGraphName,))

        return g.serialize(format="trig").decode("utf-8")

EccrevDiff.register(QuitDiffSerializer)
