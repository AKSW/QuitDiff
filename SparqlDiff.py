from abc import ABCMeta
from QuitDiffSerializer import QuitDiffSerializer


class SparqlDiff(metaclass=ABCMeta):
    """Serialize RDF deltas using Sparql Insert/Delete Queries."""

    def serialize(self, add, delete):

        deleteQuadPattern = ""
        insertQuadPattern = ""
        for graphUri, graph in delete.items():
            if len(graph) > 0:
                if str(graphUri) != 'http://quitdiff.default/':
                    deleteQuadPattern += "\ngraph <%s> {\n%s\n}\n" % (graphUri, graph.serialize(format="nt").decode("utf-8").strip())
                else:
                    deleteQuadPattern += "\n%s\n" % (graph.serialize(format="nt").decode("utf-8").strip())
        for graphUri, graph in add.items():
            if len(graph) > 0:
                if str(graphUri) != 'http://quitdiff.default/':
                    insertQuadPattern += "\ngraph <%s> {\n%s\n}\n" % (graphUri, graph.serialize(format="nt").decode("utf-8").strip())
                else:
                    insertQuadPattern += "\n%s\n" % (graph.serialize(format="nt").decode("utf-8").strip())

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
