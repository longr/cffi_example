#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name="fibonacci",
    version="0.1",
    author="Robin Long",
    author_email="robin.long@hotmail.co.uk",
    url="https://github.com/longr/cffi_example",
    description="An example package that demonstrates how to layout and create a python package, and also demonstrates how to call c code from python using CFFI.",
    packages=find_packages(),
)
