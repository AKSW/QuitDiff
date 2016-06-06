#!/usr/bin/env python3

import os
from rdflib import ConjunctiveGraph, compare
import rdflib
import argparse
from EccpatchDiff import EccpatchDiff
from SparqlDiff import SparqlDiff
from QuitDiffSerializer import QuitDiffSerializer


class QuitDiff:

    local = None
    remote = None
    merged = None
    base = None

    def __init__ (self):
        True


    def readIsomorphicGraph(self, file):
        format = rdflib.util.guess_format(file)
        graph = ConjunctiveGraph()
        graph.load(file, format=format)

        print("file:", file)
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

        print ("")
        diffSerializer = SparqlDiff()
        print("serialization:", diffSerializer.serialize(add, remove))

if __name__ == "__main__":

    # command line parameters
    # https://git-scm.com/docs/git-difftool
    # $LOCAL is set to the name of the temporary file containing the contents of the diff pre-image and
    # $REMOTE is set to the name of the temporary file containing the contents of the diff post-image.
    # $MERGED is the name of the file which is being compared.
    # $BASE is provided for compatibility with custom merge tool commands and has the same value as $MERGED.
    #
    # local is the old version
    # remote is the new version
    parser = argparse.ArgumentParser()
    parser.add_argument('--local', type=str)
    parser.add_argument('--remote', type=str)
    parser.add_argument('--merged', type=str)
    parser.add_argument('--base', type=str)

    args = parser.parse_args()

    quitdiff = QuitDiff()
    quitdiff.diff(args.local, args.remote, args.merged, args.base)
