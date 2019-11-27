#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

def get_requirements(name):
    with open(name) as f:
        return f.read().splitlines()

install_requires = []

tests_require = [
    'pytest',
    'pytest-cov',
]

docs_require = [
    'sphinx',
    'sphinx_rtd_theme',
]

linting_requires = [
    'flake8',
    'black',
    'readme_renderer',
    'check-manifest',
    'docutils',
]

setup(
    name="fibonacci",
    version="0.1",
    author="Robin Long",
    author_email="robin.long1@hotmai.co.uk",
    url="https://github.com/longr/python_packaging_example",
    description="A simple example package.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={"testing": tests_require,
                    'docs': docs_require,
                    'linting': linting_requires},
)
