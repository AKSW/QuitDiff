import click
from .QuitDiff import QuitDiff


@click.command()
@click.option('--mode', envvar="QUIT_DIFF_MODE", default="simple", help='The diff mode can be simple delta comparison (simple, default), or a three way diff (threeway)')
@click.option('--format', '--diffFormat', envvar="QUIT_DIFF_FORMAT", default="sparql", help='The serialization format to represent the differences, e.g. sparql [default], changeset, eccrev, topbraid')
@click.option('--base', envvar="BASE", default=None, help='The last common base version, to perform a three-way-merge')
@click.option('--merged', envvar="MERGED", default=None, help='merged')
@click.argument('local', envvar="LOCAL")
@click.argument('remote', envvar="REMOTE")
def cli(mode: str, format: str, base: str, merged: str, local: str, remote: str):
    """
    Compare two RDF datasets with each other.

    LOCAL is the first dataset to compare, REMOTE the second dataset to compare

    This can also be setup as [git-difftool](https://git-scm.com/docs/git-difftool)
    """

    quitdiff = QuitDiff()
    if mode == "simple":
        quitdiff.simple_diff(local, remote, diffFormat=format)
    elif mode == "threeway":
        quitdiff.threeway_diff(local, remote, base, diffFormat=format)


@click.command()
@click.option('--format', '--diffFormat', default="sparql", help='The serialization format to represent the differences, e.g. sparql [default], changeset, eccrev, topbraid')
@click.argument("path")
@click.argument("oldFile")
@click.argument("oldHex")
@click.argument("oldMode")
@click.argument("newFile")
@click.argument("newHex")
@click.argument("newMode")
def git_diff(path: str, oldfile: str, oldhex: str, oldmode: str, newfile: str, newhex: str, newmode: str, format: str):
    """
    This command can be setup as external diff driver for git.
    For the details please see the git documentation on [gitattributes](https://git-scm.com/docs/gitattributes#_defining_an_external_diff_driver)
    """

    quitdiff = QuitDiff()
    quitdiff.simple_diff(oldfile, newfile, diffFormat=format)

if __name__ == '__main__':
    cli()
