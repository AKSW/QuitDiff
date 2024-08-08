from abc import ABCMeta
from ..QuitDiff import QuitDiffSerializer
from rdflib.plugins.sparql.processor import prepareUpdate
from rdflib.plugins.sparql.algebra import pprintAlgebra

class SparqlDiff(metaclass=ABCMeta):
    """Serialize RDF deltas using Sparql Insert/Delete Queries."""
    def __init__(self):
        self.preparedUpdate = prepareUpdate("delete data {}; insert data {}")

    def serialize(self, add, delete):
        deleteQuadPattern = ""
        insertQuadPattern = ""
        for graphUri, graph in delete.items():
            if len(graph) > 0:
                # self.preparedUpdate.algebra[0].triples.extend(graph.triples((None,None,None)))
                if str(graphUri) != "http://quitdiff.default/":
                    deleteQuadPattern += "\ngraph <%s> {\n%s\n}\n" % (
                        graphUri,
                        graph.serialize(format="turtle").strip(),
                    )
                else:
                    deleteQuadPattern += "\n%s\n" % (
                        graph.serialize(format="turtle").strip()
                    )
        for graphUri, graph in add.items():
            if len(graph) > 0:
                # self.preparedUpdate.algebra[1].triples.extend(graph.triples((None,None,None)))
                if str(graphUri) != "http://quitdiff.default/":
                    insertQuadPattern += "\ngraph <%s> {\n%s\n}\n" % (
                        graphUri,
                        graph.serialize(format="turtle").strip(),
                    )
                else:
                    insertQuadPattern += "\n%s\n" % (
                        graph.serialize(format="turtle").strip()
                    )

        query = ""
        if deleteQuadPattern:
            delimiter = "\n"
            if insertQuadPattern:
                delimiter = ";\n"
            query += "delete data {%s}" % (deleteQuadPattern) + delimiter
        if insertQuadPattern:
            query += "insert data {%s}\n" % (insertQuadPattern)
        return query


SparqlDiff.register(QuitDiffSerializer)
