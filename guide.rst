========================
Python Packaging Example
========================



Introduction
============

There are lots of resources explaining how to package, test, document and otherwise implement features and styles that will make your python code better and moe sustainable.  However many of these are hidden unless you search for the exact terms, or are not specific enough, or are to specific. These guide hopes to give an opinionated (it won't suggest alternative tools, just pick ones the authors prefer and explain how to use them and only them).   This repositry itself will act as an example of all the features and suggestions.

.. contents::

Modules vs Packages
===================

In python a module is a single python file ending in `.py` that can be imported using the command `import`. Each module has its own namespace, this means that functions in this module can call each other without having to reference the modules file name. Outside of the module, such as when we import it, the module name needs to be used when calling the a function in the file, such as in the example below.

```python
import my_module
my_module.my_function()
```
Here we have imported a module named `my_module` and called a function named `my_function`.

A package is a way of collecting several modules together under another common namespace.

```python
my_package/              # Package
       __init__.py    # Initialisation file
       module_01.py   # Module 1
       module_02.py   # Module 2
```
Here we have a package named `my_package` which contains two modules imaginitivly named `module_01` and `module_02`.  When `my_package` is imported we will need to call the full function name such as `my_package.module_01.function()`.  However functions in each module only need to call the module name followed by the function such as `module_01.function()`.  

`RealPython Packages and Modules <https://realpython.com/python-modules-packages/>`_

`Packaging - PyPi <https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/contributing.html>`_

`Glossary <https://packaging.python.org/glossary/>`_

Package Layout
==============

Packages have a very simple layout.  Each module is inside a directory, the only requirements (other than standard python limits on what can be in a name) is that there must be a file called `__init__.py`. This file can be empty, or it can contain an import statement which imports each module by name. 

There is a lot of flexibility in allowed in how a python package is laid out, and two main schools of thought on how to lay them out.  We recommend using the `src` layout. Here, all python packages are 


`Python <http://www.python.org/>`_

`Structuring your project <https://docs.python-guide.org/writing/structure/>`_

`Steps to success <https://towardsdatascience.com/10-steps-to-set-up-your-python-project-for-success-14ff88b5d13>`_

`Setuptools <https://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages>`_


`Dead Simple Python: Project Structure and Imports <https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6>`_


`pypa on layout <https://github.com/pypa/packaging.python.org/issues/320>`_

Packaging - setup.py
====================

`Packaging a python library <https://blog.ionelmc.ro/2014/05/25/python-packaging/>`_

`RealPython Packages and Modules <https://realpython.com/python-modules-packages/>`_

`Build a pip packages <https://dzone.com/articles/executable-package-pip-install>`_

`Packaging - PyPi <https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/contributing.html>`_

`Packaging Python Projects <https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives>`_

`Packaging binary extensions <https://packaging.python.org/guides/packaging-binary-extensions/>`_

`Setuptools <https://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages>`_


`Practical guide to Setup.py <https://blog.godatadriven.com/setup-py>`_

.. create DOI

Running and installing the package
----------------------------------

Manifest
--------

Licence
-------

Style Guide
-----------

Contributing
------------

Testing with pytest
===================

`Packaging and Testing <https://hynek.me/articles/testing-packaging/>`_

`Hitch Hikers HGuide testing <https://docs.python-guide.org/writing/tests/>`_

`UCL <http://rits.github-pages.ucl.ac.uk/research-se-python/morea/section2/reading3.html>`_

`PyTest <https://docs.pytest.org/en/latest/>`_

`RealPython Testing <https://realpython.com/python-testing/>`_

`Good practises <https://pytest.readthedocs.io/en/2.7.3/goodpractises.html>`_



Tests and Continuous Integration
================================

`Extensive Python Testing on Travis CI <https://blog.travis-ci.com/2019-08-07-extensive-python-testing-on-travis-ci>`_

`Untold stories about python unit tests <https://hackernoon.com/untold-stories-about-python-unit-tests-a141501f0ee>`_

Test coverage
=============

`Pytest and coverage <https://stackoverflow.com/questions/21991765/how-to-generate-coverage-from-setup-py>`_

`pytest import issues <http://doc.pytest.org/en/latest/pythonpath.html#pytest-vs-python-m-pytest>`_




Codecov.io
==========

`Codecov + python + travis <https://dev.to/j0nimost/using-codecov-with-travis-ci-pytest-cov-1dfj>`_

`exclude files from codecov <https://docs.codecov.io/docs/codecov-yaml>`_
`Codecov + python + travis beginners <https://medium.com/datadriveninvestor/beginners-guide-to-using-codecov-with-python-and-travis-ci-c17659bb711>`_
`Codecov yaml <https://docs.codecov.io/docs/codecov-yaml>`_


Testing against multiple versions
=================================

Testing on multiple OS's
------------------------

`Testing Your Project on Multiple Operating Systems <https://docs.travis-ci.com/user/multi-os/>`_

`Windows build on Travis <https://docs.travis-ci.com/user/reference/windows/>`_

Documentation
=============

https://realpython.com/documenting-python-code/


CI and Docs
===========

Read the docs
-------------

Code Quality with Black
=======================

`Black - code style <https://github.com/python/black>`_


Uploading to PiPy with CI
=========================

`Upload to PyPi <https://gist.github.com/gboeing/dcfaf5e13fad16fc500717a3a324ec17>`_


Linux
-----
OSX
---
Windows
-------

Extending Python with C
=======================
Should this be a separate thing?


.. dont forget github tags and readmes.
   should we discuss github and uses?


.. https://github.com/pandas-dev/pandas  good readme layout
..      https://github.com/pandas-dev/pandas
.. https://github.com/yanqd0/csft
.. https://github.com/google/yapf/blob/master/README.rst
