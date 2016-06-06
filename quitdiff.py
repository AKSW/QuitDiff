#!/usr/bin/env python3

import argparse
from QuitDiff import QuitDiff

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
    parser.add_argument('--diffFormat', default="sparql", type=str)
    parser.add_argument('--local', type=str)
    parser.add_argument('--remote', type=str)
    parser.add_argument('--merged', type=str)
    parser.add_argument('--base', type=str)

    args = parser.parse_args()

    quitdiff = QuitDiff()
    quitdiff.diff(args.local, args.remote, args.merged, args.base, diffFormat=args.diffFormat)
