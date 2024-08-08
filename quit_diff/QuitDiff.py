from typing import Dict

import rdflib
from rdflib import ConjunctiveGraph, compare, BNode, Graph
from importlib import import_module
from os import walk
from os.path import isfile, isdir, join


class QuitDiffSerializer:
    def serialize(self, add, delete):
        return NotImplemented


class QuitDiff:
    local = None
    remote = None
    merged = None
    base = None
    nsQuitDiff = "http://quitdiff.default/"

    def readIsomorphicGraph(self, file):
        graph = ConjunctiveGraph(identifier="")

        # check if we handle a directory or a seperate file
        if isdir(file):
            # for a better readability rename variable
            dir = file
            for path, dirs, files in walk(dir):
                for dir_file in files:
                    absfile = join(path, dir_file)
                    format = rdflib.util.guess_format(absfile)

                    if format is not None:
                        graph.parse(absfile, format=format, publicID=self.nsQuitDiff)

        elif isfile(file):
            format = rdflib.util.guess_format(file)

            if format is not None:
                graph.parse(file, format=format, publicID=self.nsQuitDiff)

        contextDict = {}
        contextDict[self.nsQuitDiff] = Graph()

        for subgraph in graph.contexts():
            # TODO we have to copy all the triples to a new ConjunctiveGraph
            # because https://rdflib.readthedocs.io/en/stable/_modules/rdflib/compare.html takes the complete store
            # and thus doesn't support quads
            triples = subgraph.triples((None, None, None))
            if (
                isinstance(subgraph.identifier, BNode)
                or str(subgraph.identifier) == self.nsQuitDiff
            ):
                subgraphConjunctive = contextDict[self.nsQuitDiff]
            else:
                try:
                    subgraphConjunctive = contextDict[subgraph.identifier]
                except Exception:
                    contextDict[subgraph.identifier] = ConjunctiveGraph()
                    subgraphConjunctive = contextDict[subgraph.identifier]

            for triple in triples:
                subgraphConjunctive.add(triple)
            # end TODO hack

        graphDict = {}

        for identifier, graph in contextDict.items():
            graphDict[identifier] = compare.to_isomorphic(graph)

        return graphDict

    def simple_diff(self, local, remote, diffFormat="sparql"):
        self.local = self.readIsomorphicGraph(local)
        self.remote = self.readIsomorphicGraph(remote)

        add = {}
        remove = {}

        graphUris = set(self.local.keys()) | set(self.remote.keys())

        for uri in graphUris:
            if uri in self.local.keys() and uri in self.remote.keys():
                localGraph = self.local[uri]
                remoteGraph = self.remote[uri]
                in_both, in_first, in_second = compare.graph_diff(
                    localGraph, remoteGraph
                )
                add[uri] = in_second
                remove[uri] = in_first
            elif uri in self.local.keys():
                remove[uri] = self.local[uri]
            elif uri in self.remote.keys():
                add[uri] = self.remote[uri]
            else:
                True

        module = diffFormat.title() + "Diff"
        diff = getattr(import_module("quit_diff.serializer." + module), module)

        diffSerializer = diff()
        print(diffSerializer.serialize(add, remove))

    def threeway_diff(self, local, remote, base, diffFormat="sparql"):
        """
        Implements the three way diff on datasets.
        """
        aG = self.readIsomorphicGraph(local)
        bG = self.readIsomorphicGraph(remote)
        baseG = self.readIsomorphicGraph(base)

        aGraphUris = set(aG.keys())
        bGraphUris = set(bG.keys())
        baseGraphUri = set(baseG.keys())

        addAGraphs = aGraphUris - baseGraphUri
        delAGraphs = baseGraphUri - aGraphUris
        addBGraphs = bGraphUris - baseGraphUri
        delBGraphs = baseGraphUri - bGraphUris

        addA = {uri: aG[uri] for uri in addAGraphs}
        addB = {uri: bG[uri] for uri in addBGraphs}
        delA = {uri: baseG[uri] for uri in delAGraphs}
        delB = {uri: baseG[uri] for uri in delBGraphs}

        intersect = aGraphUris.intersection(bGraphUris)

        for uri in intersect:
            threeway_set = self.threeway_graph_diff(aG[uri], bG[uri], baseG[uri])
            addA[uri] = threeway_set["addA"]
            addB[uri] = threeway_set["addB"]
            delA[uri] = threeway_set["delA"]
            delB[uri] = threeway_set["delB"]

        module = diffFormat.title() + "Diff"
        diff = getattr(import_module("quit_diff.serializer." + module), module)

        diffSerializer = diff()
        print(diffSerializer.serialize(addA, delA))
        print(diffSerializer.serialize(addB, delB))

    def threeway_graph_diff(self, local: Graph, remote: Graph, base: Graph) -> Dict:
        """
        Implements the three way diff on datasets.
        """

        a = set(local.triples((None, None, None)))
        b = set(remote.triples((None, None, None)))
        base_set = set(base.triples((None, None, None)))

        addA = a - base_set
        delA = base_set - a
        addB = b - base_set
        delB = base_set - b

        addAGraph = Graph()
        for t in addA:
            addAGraph.add(t)

        delAGraph = Graph()
        for t in delA:
            delAGraph.add(t)

        addBGraph = Graph()
        for t in addB:
            addBGraph.add(t)

        delBGraph = Graph()
        for t in delB:
            delBGraph.add(t)


        return {
            "addA": addAGraph,
            "delA": delAGraph,
            "addB": addBGraph,
            "delB": delBGraph,
        }

    def merge(self, local, remote, merged, base, diffFormat="sparql"):
        # TODO
        if local:
            self.local = self.readIsomorphicGraph(local)

        if remote:
            self.remote = self.readIsomorphicGraph(remote)

        if merged:
            self.merged = self.readIsomorphicGraph(merged)

        if base:
            self.base = self.readIsomorphicGraph(base)

        add = {}
        remove = {}
        # TODO

        graphUris = set(self.local.keys()) | set(self.remote.keys())

        for uri in graphUris:
            if uri in self.local.keys() and uri in self.remote.keys():
                localGraph = self.local[uri]
                remoteGraph = self.remote[uri]
                in_both, in_first, in_second = compare.graph_diff(
                    localGraph, remoteGraph
                )
                add[uri] = in_second
                remove[uri] = in_first
            elif uri in self.local.keys():
                remove[uri] = self.local[uri]
            elif uri in self.remote.keys():
                add[uri] = self.remote[uri]
            else:
                True

        module = diffFormat.title() + "Diff"
        diff = getattr(import_module("quit_diff.serializer." + module), module)

        diffSerializer = diff()
        print(diffSerializer.serialize(add, remove))
