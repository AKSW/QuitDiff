

import rdflib
from rdflib import ConjunctiveGraph, compare
from QuitDiffSerializer import QuitDiffSerializer
from importlib import import_module
from os import listdir
from os.path import isfile, isdir, join

class QuitDiff:

    local = None
    remote = None
    merged = None
    base = None

    def __init__ (self):
        True


    def readIsomorphicGraph(self, file):
        graph = ConjunctiveGraph()

        # check if we handle a directory or a seperate file
        if isdir(file):
            # for a better readability rename variable
            dir = file
            onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
            for file in onlyfiles:
                absfile = join(dir, file)
                format = rdflib.util.guess_format(absfile)
                if format is not None:
                    graph.parse(absfile, format=format)
        elif isfile(file):
            format = rdflib.util.guess_format(file)
            if format is not None:
                graph.load(file, format=format)

        graphDict = {}
        for subgraph in graph.contexts():
            # TODO we have to copy all the triples to a new ConjunctiveGraph
            # because https://rdflib.readthedocs.io/en/stable/_modules/rdflib/compare.html takes the complete store
            # and thus doesn't support quads
            triples = subgraph.triples((None, None, None))
            subgraphConjunctive = ConjunctiveGraph()
            for triple in triples:
                subgraphConjunctive.add(triple)
            # end TODO hack

            graphDict[subgraph.identifier] = compare.to_isomorphic(subgraphConjunctive)
        return graphDict


    def diff (self, local, remote, merged, base, diffFormat='sparql'):
        print("local:", local)
        print("remote:", remote)
        print("merged:", merged)
        print("base:", base)

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

        graphUris = set(self.local.keys()) | set(self.remote.keys())
        print ("all available graphs:", graphUris)

        for uri in graphUris:
            print("graph:", uri)
            if uri in self.local.keys() and uri in self.remote.keys():
                localGraph = self.local[uri]
                remoteGraph = self.remote[uri]
                in_both, in_first, in_second = compare.graph_diff(localGraph, remoteGraph)
                add[uri] = in_second
                remove[uri] = in_first
            elif uri in self.local.keys() :
                remove[uri] = self.local[uri]
            elif uri in self.remote.keys() :
                add[uri] = self.remote[uri]
            else :
                True

        module = diffFormat.title() + "Diff"
        diff = getattr(import_module(module), module)

        print ("")
        diffSerializer = diff()
        print("serialization:", diffSerializer.serialize(add, remove))
