#!/usr/bin/env python

from distutils.util import convert_path
from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup, find_packages

main_ns = {}
ver_path = convert_path('network_tools/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name="network_tools",
    version=main_ns['__VERSION__'],
    packages=find_packages(),

    author="Matthew Pounsett",
    author_email="matt@conundrum.com",
    description="Network Tools",
    license="NONE",
    keywords="game",

    long_description="""
    network_tools

    """,

    install_requires=[
        str(x.req) for x in parse_requirements('requirements.txt',
                                               session=PipSession())
    ],
)
