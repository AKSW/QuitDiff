from abc import ABCMeta
from QuitDiffSerializer import QuitDiffSerializer

class SparqlDiff(metaclass=ABCMeta):
    def serialize(self, add, delete):

        deleteQuadPattern = ""
        insertQuadPattern = ""
        for graphUri, graph in delete.items():
            if len(graph) > 0:
                deleteQuadPattern += "\ngraph <%s> {\n%s\n}\n" % (graphUri, graph.serialize(format="nt").decode("utf-8").strip())
        for graphUri, graph in add.items():
            if len(graph) > 0:
                insertQuadPattern += "\ngraph <%s> {\n%s\n}\n" % (graphUri, graph.serialize(format="nt").decode("utf-8").strip())

        query = ""
        if deleteQuadPattern:
            query += "delete data {%s}\n" % (deleteQuadPattern)
        if insertQuadPattern:
            query += "insert data {%s}\n" % (insertQuadPattern)
        return query

SparqlDiff.register(QuitDiffSerializer)
