#!/usr/bin/env python3

import argparse
from QuitDiff import QuitDiff

if __name__ == "__main__":

    # command line parameters
    # This tool can be used for git-diff or as git-difftool
    # git-diff:
    #   if using as git-diff, the parameters are:
    #   path old-file old-hex old-mode new-file new-hex new-mode
    # git-difftool:
    #   https://git-scm.com/docs/git-difftool
    #   $LOCAL is set to the name of the temporary file containing the contents of the diff pre-image and
    #   $REMOTE is set to the name of the temporary file containing the contents of the diff post-image.
    #   $MERGED is the name of the file which is being compared.
    #   $BASE is provided for compatibility with custom merge tool commands and has the same value as $MERGED.
    #
    # local is the old version
    # remote is the new version
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', type=str)
    parser.add_argument('oldFile', nargs='?', type=str)
    parser.add_argument('oldHex', nargs='?', type=str)
    parser.add_argument('oldMode', nargs='?', type=str)
    parser.add_argument('newFile', nargs='?', type=str)
    parser.add_argument('newHex', nargs='?', type=str)
    parser.add_argument('newMode', nargs='?', type=str)
    parser.add_argument('--diffFormat', default="sparql", type=str)
    parser.add_argument('--local', type=str)
    parser.add_argument('--remote', type=str)
    parser.add_argument('--merged', type=str)
    parser.add_argument('--base', type=str)

    args = parser.parse_args()

    quitdiff = QuitDiff()
    if (args.path):
        quitdiff.diff(args.path, args.oldFile, args.newFile, diffFormat=args.diffFormat)
    elif (args.local and args.remote):
        quitdiff.difftool(args.local, args.remote, args.merged, args.base, diffFormat=args.diffFormat)
    else:
        parser.print_help()
        exit(1)
