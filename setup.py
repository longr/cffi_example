#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(name='fibonacci',
      version='0.1',
      author='Robin Long',
      author_email='robin.long@hotmail.co.uk',
      url='https://github.com/longr/cffi_example',
      description='An example package that demonstrates how to layout and create a python package, and also demonstrates how to call c code from python using CFFI.',
      packages=find_packages(),
      setup_requires=['cffi','pytest-runner'],
      test_require=['pytest'],
      cffi_modules=['fibonacci/build_fibonacci.py:ffi'],
      include_dirs=['src'],
      install_requires=['cffi'],
      keywords='python cffi example c-code',
      # license='need one',
      # fibonacci has C extensions, so it is not zip safe.
      # Telling setuptools this prevents it from doing an automatic
      # check for zip safety.
#      zip_safe=False,
)
