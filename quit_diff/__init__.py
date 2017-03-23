import argparse
from .QuitDiff import QuitDiff
from .QuitDiff import QuitDiffSerializer

def main(args=None):

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
        exit(1)
