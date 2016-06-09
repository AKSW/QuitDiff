# Quit Diff

## Use as `git-difftool`

Add one of the following sections to you `~/.gitconfig` (in your home directory) or `.git/config` (in your git working directory).

    [difftool "quitdiff"]
        cmd = quitdiff.py --local=\"$LOCAL\" --remote=\"$REMOTE\" --merged=\"$MERGES\" --base=\"$BASE\"


    [difftool "quitdiff-sparql"]
        cmd = quitdiff.py --diffFormat sparql --local=\"$LOCAL\" --remote=\"$REMOTE\" --merged=\"$MERGES\" --base=\"$BASE\"

    [difftool "quitdiff-eccrev"]
        cmd = quitdiff.py --diffFormat eccrev --local=\"$LOCAL\" --remote=\"$REMOTE\" --merged=\"$MERGES\" --base=\"$BASE\"

The git diff tool can then called with one of the following commands

    $ git difftool -t quitdiff
    $ git difftool -t quitdiff HEAD~0..HEAD~2

## Use as `git-diff`

Add the following sections to you `~/.gitconfig` (in your home directory) or `.git/config` (in your git working directory).

    [diff "quitdiff"]
        command = quitdiff.py

and the following to `.gitattributes`  (in your git working directory).

    *.nq diff=quitdiff
    *.trig diff=quitdiff
    *.nt diff=quitdiff
    *.ttl diff=quitdiff
    *.rdf diff=quitdiff

git diff can then called with one of the following commands

    $ git diff
    $ git diff HEAD~0..HEAD~2
