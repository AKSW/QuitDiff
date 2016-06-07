# Quit Diff

Add one of the following sections to you `~/.gitconfig` (in your home directory).
    [difftool "quitdiff"]
        cmd = quitdiff.py --local=\"$LOCAL\" --remote=\"$REMOTE\" --merged=\"$MERGES\" --base=\"$BASE\"


    [difftool "quitdiff-sparql"]
        cmd = quitdiff.py --diffFormat sparql --local=\"$LOCAL\" --remote=\"$REMOTE\" --merged=\"$MERGES\" --base=\"$BASE\"

    [difftool "quitdiff-eccrev"]
        cmd = quitdiff.py --diffFormat eccrev --local=\"$LOCAL\" --remote=\"$REMOTE\" --merged=\"$MERGES\" --base=\"$BASE\"
