"""

"""
from distutils.util import convert_path
from setuptools import setup, find_packages

main_ns = {}
ver_path = convert_path('netmath/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name="netmath",
    version=main_ns['__VERSION__'],
    packages=find_packages(),

    author="Matthew Pounsett",
    author_email="matt@conundrum.com",
    description="Network Tools",
    license="Apache Software License 2.0",
    keywords="network library",

    long_description=__doc__,

    install_requires=[
    ],
)
