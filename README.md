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

# License

Copyright (C) 2017 Natanael Arndt <http://aksw.org/NatanaelArndt> and Norman Radtke <http://aksw.org/NormanRadtke>

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses>.
Please see [LICENSE](LICENSE) for further information.
