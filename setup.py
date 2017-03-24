#!/usr/bin/env python

from distutils.core import setup

setup(
    name='QuitDiff',
    version='1.0.1',
    description='A git difftool for RDF data',
    author='Natanael Arndt, Norman Radtke',
    author_email='arndt@informatik.uni-leipzig.de, radtke@informatik.uni-leipzig.de',
    license='GNU General Public License Version 3',
    url='https://github.com/AKSW/QuitDiff',
    download_url='https://github.com/AKSW/QuitDiff/archive/master.tar.gz',
    install_requires=[
        'rdflib==4.2.1'
    ],
    dependency_links=[
        'rdflib==4.2.1'
    ],
    packages=[
        'quit_diff',
        'quit_diff.serializer'
    ]
)
