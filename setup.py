#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="fibonacci",
    version="0.1",
    author="Robin Long",
    author_email="robin.long1@hotmai.co.uk",
    url="https://github.com/longr/python_packaging_example",
    description="A simple example package.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    tests_require=["pytest"],
    extras_require={"testing": ["pytest", "pytest-cov"]},
)
