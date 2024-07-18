# Quit Diff

## Requirements

For using QuitDiff you need to have python version 3 installed (3.9 or later).

To install the required packages use pip:

```
pipx install quit-diff
```

## Use as `git-difftool`

Add one of the following sections to you `~/.gitconfig` (in your home directory) or `.git/config` (in your git working directory).

```
[difftool "quit-diff"]
    cmd = quit-diff --base=\"$BASE\" \"$LOCAL\" \"$REMOTE\"
```

The git diff tool can then called with one of the following commands

```
$ git difftool -t quit-diff
$ git difftool -t quit-diff HEAD~0..HEAD~2
```

To specify the diff format you can set the `QUIT_DIFF_FORMAT` environment variable.

```
$ QUIT_DIFF_FORMAT=changeset git difftool -t quit-diff HEAD^
$ QUIT_DIFF_FORMAT=sparql git difftool -t quit-diff HEAD^
$ QUIT_DIFF_FORMAT=eccrev git difftool -t quit-diff HEAD^
```

## Use as `git diff`

Add the following sections to you `~/.gitconfig` (in your home directory) or `.git/config` (in your git working directory).

```
[diff "quit-diff"]
    command = quit-diff
```

and the following to `.gitattributes`  (in your git working directory).

```
*.nq diff=quit-diff
*.trig diff=quit-diff
*.nt diff=quit-diff
*.ttl diff=quit-diff
*.rdf diff=quit-diff
```

git diff can then called with one of the following commands

```
$ git diff
$ git diff HEAD~0..HEAD~2
```


# Command line parameters
This tool can be used for git-diff or as git-difftool

## git-diff:
if using as git-diff, the parameters are: `path old-file old-hex old-mode new-file new-hex new-mode`

## git-difftool:
https://git-scm.com/docs/git-difftool
* $LOCAL is set to the name of the temporary file containing the contents of the diff pre-image and
* $REMOTE is set to the name of the temporary file containing the contents of the diff post-image.
* $MERGED is the name of the file which is being compared.
* $BASE is provided for compatibility with custom merge tool commands and has the same value as $MERGED.

* local is the old version
* remote is the new version

# License

Copyright (C) 2024 Natanael Arndt <http://aksw.org/NatanaelArndt> and Norman Radtke <http://aksw.org/NormanRadtke>

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses>.
Please see [LICENSE](LICENSE.txt) for further information.
