from abc import ABCMeta
from ..QuitDiff import QuitDiffSerializer
from rdflib import BNode, Namespace, ConjunctiveGraph
from rdflib.namespace import RDF, NamespaceManager
import uuid


class ChangesetDiff(metaclass=ABCMeta):
    def serialize(self, add, delete):


        changeset = Namespace("http://purl.org/vocab/changeset/schema#")
        #@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        g = ConjunctiveGraph()

        namespace_manager = NamespaceManager(g)
        namespace_manager.bind('changeset', changeset, override=False)

        graphUris = set(delete.keys()) | set(add.keys())

        for graphUri in graphUris:
            if (graphUri in delete.keys() and len(delete[graphUri]) > 0) or (graphUri in add.keys() and len(add[graphUri]) > 0):
                diff = Namespace("urn:changeset:" + str(uuid.uuid1()))
                graphTerm = diff.term("")
                g.add( (graphTerm, RDF.type, changeset.ChangeSet) )
                if str(graphUri) != 'default':
                    g.add( (graphTerm, changeset.subjectOfChange, graphUri) )
                if graphUri in delete.keys() and len(delete[graphUri]) > 0:
                    i = 0
                    for triple in delete[graphUri]:
                        deleteStatementName = BNode()
                        g.add( (graphTerm, changeset.removal, deleteStatementName) )
                        g.add( (deleteStatementName, RDF.type, RDF.Statement) )
                        g.add( (deleteStatementName, RDF.subject, triple[0]) )
                        g.add( (deleteStatementName, RDF.predicate, triple[1]) )
                        g.add( (deleteStatementName, RDF.object, triple[2]) )
                        i += 1
                if graphUri in add.keys() and len(add[graphUri]) > 0:
                    i = 0
                    for triple in add[graphUri]:
                        insertGraphName = BNode()
                        g.add( (graphTerm, changeset.addition, insertGraphName) )
                        g.add( (insertGraphName, RDF.type, RDF.Statement) )
                        g.add( (insertGraphName, RDF.subject, triple[0]) )
                        g.add( (insertGraphName, RDF.predicate, triple[1]) )
                        g.add( (insertGraphName, RDF.object, triple[2]) )
                        i += 1

        return g.serialize(format="turtle").decode("utf-8")

ChangesetDiff.register(QuitDiffSerializer)
