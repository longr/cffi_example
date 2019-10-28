========================
Python Packaging Example
========================

Introduction
============

There are lots of resources explaining how to package, test, document and otherwise implement features and styles that will make your python code better and moe sustainable.  However many of these are hidden unless you search for the exact terms, or are not specific enough, or are to specific. These guide hopes to give an opinionated (it won't suggest alternative tools, just pick ones the authors prefer and explain how to use them and only them).   This repositry itself will act as an example of all the features and suggestions.

In the following tutorial we will build a package named `fibonacci` that contains a single function named `fib`.  We shall put this into a package, and then add tests, documentation and take you through the other steps needed to turn our file into a full python package which adhers to all best practises in writing python code and reproducible and sustainable software.

.. contents::

Modules and Packages
===================

.. In python modules are just python, `.py`, files. Packages are collections of modules in a directory with an `__init__.py` file in it.  
.. Could this be written less formally?

In python a module is a single python file ending in `.py` that can be imported using the command `import`. Each module has its own namespace, this means that functions in this module can call each other without having to reference the modules file name. Outside of the module, such as when we import it, the module name needs to be used when calling the a function in the file, such as in the example below.

```python
import fibonacci
fibonacci.fib(3)
# 2
```
Here we have imported a module named `my_module` and called a function named `my_function`.

A package is a way of collecting several modules together under another common namespace.

```python
fibonacci/              # Package
       __init__.py    # Initialisation file
       module_02.py   # Module 2
```
Here we have a package named `my_package` which contains two modules imaginitivly named `module_01` and `module_02`.  When `my_package` is imported we will need to call the full function name such as `my_package.module_01.function()`.  However functions in each module only need to call the module name followed by the function such as `module_01.function()`.  

.. `RealPython Packages and Modules <https://realpython.com/python-modules-packages/>`_

.. `Packaging - PyPi <https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/contributing.html>`_

.. `Glossary <https://packaging.python.org/glossary/>`_

Package Layout
==============

Packages have a very simple layout.  Each module is inside a directory, the only requirements (other than standard python limits on what can be in a name) is that there must be a file called `__init__.py`. This file can be empty, or it can contain an import statement which imports each module by name. 

There is a lot of flexibility in allowed in how a python package is laid out, and two main schools of thought on how to lay them out.  We recommend using the `src` layout. Here, all python packages are placed inside a directory called `src`. Then later when we get to tests and documentation, they are placed in their respective directories of `tests` and `docs`.  This gives a layout like so:

```bash
project
|--docs
|--src
|   `--my_package
|          |-- __init__.py
|          `-- my_module
`--tests
```

This layout will help when it comes to testing later on. For a description of why this layout is better see `Testing and Packaging by Hynek Schlawack <https://hynek.me/articles/testing-packaging/>`_.  For now we shall create our package layout and our files.

First lets create the directory layout

```bash
mkdir -p fibonacci-project/src/fibonacci
```
and then create our module file inside `src/fibonacci` which we will call `fibonacci`.

```python
def fib(n):
    a, b = 0, 1
    fib_number = 1
    if n < 2:
        return n
    while fib_number < n:
        a, b = b, a + b
	fib_number += 1
    return b
```

we will then need to create an `__init__.py` to turn our directory with a module into a package.  The init file only needs to import our single module.

`__init__.py` file
```python
import fibonacci
```

Importing modules
-----------------

To test our package we can now import it. Since our package is located inside the `src` directory we cannot just import it as `import fibonacci` and as `src` does not contain and `__init__.py` we cannot import that either.  We need to move into the `src` directory (this is only needed for this quick test and example. In the next section we will create a `setup.py` file that will allow us to install our package so we don't have to be in the `src` directory.

```bash
cd src/
ipython
```

In the command above we move into the `src` directory and then start python.  We could use just `python` but the tab completion and other features that come with `ipython` make it far easier to use.

```python
import fibonacci
```

we can then call our function by doing

```python
fibonacci.fibonacci.fib(3)
```

this looks repetative and redundant, as we have two instances of 'fibonacci' in this function call. This is because the first fibonacci is the package (`fibonacci/`) and the second is the module (`fibonacci.py`). Both of these are namespaces used. We can avoid this long function call in a different ways:

We could import the module from the package:

```python
from fibonacci import fibonacii
fibonacci.fib(3)
```

or we could import the module directly

```python
import fibonacci.fibonacci
fibonacci.fib(3)
```


it would be easier for the users of our package if they did not have to do this when importing our package. To avoid this we can change the contents of out `__init__.py` to import functions from our modules into the package which would allow us to call the function like so:

```python
import fibonacci
fibonacci.fib(3)
```

There are two ways to do this. We can import an individual function or we can import the whole of a module. It is far easier to import the whole module, that way we don't have to remember to update `__init__.py` each time we create a new object (recalling that everything, function, classes, and variables are objects in python).  The downide to this is that you then cannot have two functions of the same name in different modules as they will lose their module namespace and only have teh packages namespace. It would also mean that users have access to all objects in our modules, which we may not want.  In which case we can use the second method and import just the function from out module.

to import the whole module out `__init__.py` should look like this:

```python
# import all the objects in the module 'fibonacci'
from .fibonacci import *
```
note that the leading dot is needed (in python 3) to tell python where to begin looking for a module, and the asterix means all.

to only import a single function (which makes little difference in our example as we only have one) we do this:


```python
# import just the named modules from 'fibonacci'
from .fibonacci import fib
```

when someone imports fibonacci and calls `fibonacci.fib(3)` the action of importing and calling is the same for both. In the second `__init__.py` they will only have access to the named objects though.

.. `Python <http://www.python.org/>`_

.. `Structuring your project <https://docs.python-guide.org/writing/structure/>`_

.. `Steps to success <https://towardsdatascience.com/10-steps-to-set-up-your-python-project-for-success-14ff88b5d13>`_

`Setuptools <https://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages>`_

.. `Dead Simple Python: Project Structure and Imports <https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6>`_

.. `pypa on layout <https://github.com/pypa/packaging.python.org/issues/320>`_

Packaging - setup.py
====================

.. discuss creating setup.py and import.
.. need to be inside src to do import.
   discuss types of import and need to rename files.
   
In the current way our package is structured, we have to be in the `src` directory in order to import our package into python. This makes it very hard to distribute or even use our package.  To solve this we will create a `setup.py` file in our project directory which will use the `setuptools` package to allow us to install our package using the package managment system `pip`. 

`setup.py` files can get very complicated in big projects, and if you look at the `setup.py` file for something like numpy, it runs to many lines. Luckily, for small projects we don't need such a complicated file and to create it we essentailly have to just answer a few questions, that hopefully we know as the creator of our package.

Lets look at the `setup.py` file we need for our 'fibonacci' package.

```python
from setuptools import setup, find_packages

setup(
    name="fibonacci",
    version="0.1",
    author="Robin Long",
    author_email="robin.long1@hotmai.co.uk"
    url="https://github.com/longr/python_packaging_example",
    description="A simple package containing a single module with a single function that finds the nth fibonacci number.",
    packages=find_packages(where="src"),
)

There are quite a few things here so lets look at them.

* `name`: This is pretty self descriptive, it is just the name we wish to give the package. If we are going to upload this to PyPi it needs to be unique.
* `version`: This is where you specify the version number.
* `author`: Author or authors name(s).
* `author_email`: email address(es) of the author(s).
* `description`: Here we have a description of the package, this can be as short or as long as you need.  If it is particularly long, it might be best to split it out as a separate variable and set description equal to it.
* `packages`: This needs to be the path to our package directory.  `setuptools` contains lots of helpful functions, and one of those is `find_packages` which will search in a given directory, in our case `src` and look for any directory that looks like a package. This is the only line you should change for your own package, the rest should be customised as needed.

It is worth noting that the main function we call takes a series of comma separated arguments. It is quite happy to have comma after the last argument which makes adding and removing arguments easier.
  
.. `Packaging a python library <https://blog.ionelmc.ro/2014/05/25/python-packaging/>`_

.. `RealPython Packages and Modules <https://realpython.com/python-modules-packages/>`_

.. `Build a pip packages <https://dzone.com/articles/executable-package-pip-install>`_

.. `Packaging - PyPi <https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/contributing.html>`_

.. `Packaging Python Projects <https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives>`_

.. `Packaging binary extensions <https://packaging.python.org/guides/packaging-binary-extensions/>`_

.. `Setuptools <https://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages>`_

.. `Practical guide to Setup.py <https://blog.godatadriven.com/setup-py>`_

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
