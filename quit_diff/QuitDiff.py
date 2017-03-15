#!/usr/bin/env python3

import rdflib
from rdflib import ConjunctiveGraph, compare, BNode, Graph
from rdflib.store import Store
from importlib import import_module
from os import listdir
from os.path import isfile, isdir, join


class QuitDiffSerializer:
    def serialize(self, add, delete):
        return NotImplemented

class QuitDiff:

    local = None
    remote = None
    merged = None
    base = None

    def __init__(self):
        True

    def readIsomorphicGraph(self, file):
        graph = ConjunctiveGraph(identifier='default')

        # check if we handle a directory or a seperate file
        if isdir(file):
            # for a better readability rename variable
            dir = file
            onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
            for file in onlyfiles:
                absfile = join(dir, file)
                format = rdflib.util.guess_format(absfile)

                if format is not None:
                    graph.parse(absfile, publicID='default', format=format)

        elif isfile(file):
            format = rdflib.util.guess_format(file)
            if format is not None:
                graph.parse(file, format=format)

        contextDict = {}
        contextDict['default'] = Graph()

        for subgraph in graph.contexts():
            # TODO we have to copy all the triples to a new ConjunctiveGraph
            # because https://rdflib.readthedocs.io/en/stable/_modules/rdflib/compare.html takes the complete store
            # and thus doesn't support quads
            triples = subgraph.triples((None, None, None))
            if isinstance(subgraph.identifier, BNode) or str(subgraph.identifier) == 'default':
                subgraphConjunctive = contextDict['default']
            else:
                try:
                    subGraphConjunctive = contextDict[subgraph.identifier]
                except:
                    contextDict[subgraph.identifier] = ConjunctiveGraph()
                    subgraphConjunctive = contextDict[subgraph.identifier]

            for triple in triples:
                subgraphConjunctive.add(triple)
            # end TODO hack

            for triple in triples:
                subgraphConjunctive.add(triple)

        graphDict = {}

        for identifier, graph in contextDict.items():
            graphDict[identifier] = compare.to_isomorphic(graph)

        return graphDict

    def diff (self, path, oldFile, newFile, diffFormat='sparql'):
        self.difftool(oldFile, newFile, None, None, diffFormat=diffFormat)

    def difftool (self, local, remote, merged, base, diffFormat='sparql'):

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

        for uri in graphUris:
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
        diff = getattr(import_module('quit_diff.serializer.' + module), module)

        diffSerializer = diff()
        print(diffSerializer.serialize(add, remove))
