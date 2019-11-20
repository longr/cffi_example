========================
Python Packaging Example
========================


Layout
Packaging (setup.py)
Testing (Pytest) (setup.cfg)
Coverage (Pytest-cov) (setup.cfg)
Testing with CI (Pytest + Travis) (setup.cfg, .travis.yml)
Coverage with CI (Pytest + Travis + Codecov.io) (setup.cfg, .travis.yml, .codecov.yml?)

With tox

Testing (Pytest)
Testing in Venv (Pytest + tox) (tox.ini)
Coverage (Pytest-cov) (tox.ini)
Testing with CI (Pytest + Travis) (tox.ini, .travis.yml)
Coverage with CI (Pytest + Travis + Codecov.io) (tox.ini, .travis.yml, .codecov.yml?)





Should we push tox?  Seems problematic and overkill. Not sure I like it.

Then need to look at Docs.


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

Packaging
=========


setup.py
--------
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
    author_email="robin.long1@hotmai.co.uk",
    url="https://github.com/longr/python_packaging_example",
    description="A simple package containing a single module with a single function that finds the nth fibonacci number.",
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    install_requires=[""]
)
```

There are quite a few things here so lets look at them.

* `name`: This is pretty self descriptive, it is just the name we wish to give the package. If we are going to upload this to PyPi it needs to be unique.
* `version`: This is where you specify the version number.
* `author`: Author or authors name(s).
* `author_email`: email address(es) of the author(s).
* `description`: Here we have a description of the package, this can be as short or as long as you need.  If it is particularly long, it might be best to split it out as a separate variable and set description equal to it.
* `packages`: This needs to be the path to our package directory.  `setuptools` contains lots of helpful functions, and one of those is `find_packages` which will search in a given directory, in our case `src` and look for any directory that looks like a package. This is the only line you should change for your own package, the rest should be customised as needed.
* `package_dir`: This takes a dictionary with `""` as the key, and the directory our package is in as the value.
* `install_requires` takes a python list of packages that our package depends on. At the minute we have no dependencies so it is blank.
  .. What does package_dir do?


It is worth noting that the main function we call, `setup()`, takes a series of comma separated arguments. It is quite happy to have comma after the last argument which makes adding and removing arguments easier.
  
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

Now that we have created our `setup.py` we can install and test our package.  To install our package we need to build it. This will create a tar.gz (or zip) file in a directory called `dist`.  This is a source distribution.  We can send this file to people and they will be able to install our package.

To build the package, from our root directory (the one with the `setup.py` file in it), we need to use the command:

```bash
python setup.py sdist
```

This will build the source distribution for us. The tar file that is created will be named *<package_name>-<version>* both of these values are taken from the lines in `setup.py`.  To install the package we just need to use pip.

```bash
pip install dist/fibonacci-0.1.tar.gz --user
```

..Note if you are working inside a virtual enviroment (don't worry if you don't know what one is) you won't need the `--user` flag.  This flag ensure that the package is installed to your local area and not system wide.

We can now open up a python terminal and test our package:

```python
import fibonacci
fibonacci.fib(10)
# 55
```

NOTE: We will have to rebuild the source distribution, and reinstall it every time we make changes to our package. 

Build and distribute
--------------------

If we are not wanting to distribute our package (yet), then we can skip the build step and let `pip` do this for us in a temporary directory and install it in one command.

Again, from the root directory,
```bash
pip install . --user
```
will build and install our package. As before, we will have to reinstall each time we make changes to our package.  We can skip this step by installing it in development or editable mode.  In this situation (as long as we are only python with no C/C++ code) we can edit our package and the changes will appear in our package as soon as we import it.

```bash
pip install -e . --user
```

We can test this by making a quick change to our `fibonacci.py` file.

.. Should these go here? or just before distributing on PyPi?

If we don't care about quality or whether our software is sustainable, then we can skip to "Distributing our Package".  However, we should be concerned with this, and as this is primarily aimed at researchers, we need to be concerned with this. So read on to the next sections about how to ensure our software is sustainable, and our research is reproducible.

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

.. Might have to include tox, might not be any other option.

We have written some software which is great. The software above does very little, but any you are writing for yourself will probably be to do research whose results can be published, or to produce software that can be published that will help other people do research. In which case the publishers and users (and you) need to have faith that the software works as it is meant to.  Since we are researchers we don't want to go on faith alone, we want facts. We do this by testing our code.

We can have these assurances by testing our code rigourously. There are many ways to do this, but the easiest and best is to use a testing framework for our chosen language.  For python there are a few options but (in the biased way this was intended and is written) we will look at **pytest**.

`pytest` does not come in the standard python library, so we will need to install it first.

```bash
pip install pytest --user
```
Layout
------

Pytest supports two styles of layouts, as always we will look at just one.

```bash
project
|--src
|   `--my_package
|          |-- __init__.py
|          `-- my_module
`--tests
    `--test_my_module.py
```
Using this layout, pytest will be able to find and run your tests against your code. All tests should go in files beginning `test_` and should be inside our `test` directory.

Writing tests
-------------
Pytest is a very powerful program, yet it has a simple syntax.

Now that we have our layout, We can create the file `test/test_fibonacci.py` and put some tests in it to see if our code works.

```python
# contents of test_fibonacci.py
import pytest
import fibonacci

def test_fib_check_zero():
    assert fibonacci.fib(0) == 0
```

To run these tests we need to call `pytest` on the command line.

```bash
pytest
========================================== test session starts ==========================================
platform linux -- Python 3.7.5, pytest-5.2.1, py-1.8.0, pluggy-0.12.0
rootdir: /home/user/python_packaging_example
plugins: flakes-4.0.0, cov-2.8.1, pep8-1.0.6
collected 1 item                                                                                        

tests/test_fibonacci.py .                                                                         [100%]

=========================================== 1 passed in 0.02s ===========================================
```

Pytest found our test file (`tests/test_fibonacci.py`) and 1 test (indicated by the '.' after the file name).  It was that simple, but now lets look at the test file in more detail.

The first thing we need to do is import the modules we need; at a minimum these should be pytest and our package, but we may need more depending on what we need to do.

We then need to write our tests. Each test should begin with `test_`. Naming them like this ensures that **pytest** can find them. They should have a decriptive name that tells us what the test does, such as what function is called and what we are testing it for. The test function is then very simple. We can conduct many different tests in these functions, many of which are beyond the scope of this guide. We shall just look at assert for now.  `assert` will check that a conditional expression evaluates to `true`. In our case we have stated that `fibonnaci.fib(0) == 0`. When this function is run, a test will pass if the conditional evaluates to true.


Integration with setuptools
---------------------------

We can integrate `pytest` with setuptools; this will allow setuptools to download pytest if needed, and build the package first if this is needed.  To do this we need to create a file called `setup.cfg` with the following contents:

```bash
[aliases]
test=pytest
```

This tells setuptools to call pytest instead of the default test. To run our tests we now call the command:

```bash
python setup.py test
```

We can run pytest with extra arguments, such as `--verbose` which will print out more information about our tests.  We could just type this on the command line as `pytest --verbose`, but since we have already integreated pytest into setuptools, we should add this flag to `setup.cfg` - lets edit it and add a few extra lines.

```bash
[aliases]
test=pytest

[tool:pytest]
addopts = --verbose
```

We also need to update `setup.py` to let it know that our package depends on `pytest` for running tests. This will mean that it can download and install `pytest` if needed.  We just need to add one line `tests_require=["pytest"],` if we need other packages for running our tests that are not already required by our package, we need to include them here. `tests_requires` takes a python list of strings. Our setup.py should now look like this:

```python
from setuptools import setup, find_packages

setup(
    name="fibonacci",
    version="0.1",
    author="Robin Long",
    author_email="robin.long1@hotmai.co.uk",
    url="https://github.com/longr/python_packaging_example",
    description="A simple package containing a single module with a single function that finds the nth fibonacci number.",
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    install_requires=[""],
    tests_requires=["pytest"],
)
```

Now when we run the tests we get more information

```bash
$ python3 setup.py test
running pytest
running egg_info
writing src/fibonacci.egg-info/PKG-INFO
writing dependency_links to src/fibonacci.egg-info/dependency_links.txt
writing top-level names to src/fibonacci.egg-info/top_level.txt
reading manifest file 'src/fibonacci.egg-info/SOURCES.txt'
writing manifest file 'src/fibonacci.egg-info/SOURCES.txt'
running build_ext

========================================== test session starts ==========================================
platform linux -- Python 3.7.5, pytest-5.2.1, py-1.8.0, pluggy-0.12.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/user/python_packaging_example, inifile: setup.cfg
plugins: flakes-4.0.0, cov-2.8.1, pep8-1.0.6
collected 1 item                                                                                        

tests/test_fibonacci.py::test_fib_check_zero PASSED                                               [100%]

=========================================== 1 passed in 0.02s ===========================================

As we can see, the package is built first, and then the tests are ran.  We also get more detail now, and instead of a dot ('.') representing each function, each function is named and put on a separate line.

.. init.py in tests
.. Use hypothesis?
   

`Packaging and Testing <https://hynek.me/articles/testing-packaging/>`_

`Hitch Hikers HGuide testing <https://docs.python-guide.org/writing/tests/>`_

`UCL <http://rits.github-pages.ucl.ac.uk/research-se-python/morea/section2/reading3.html>`_

`PyTest <https://docs.pytest.org/en/latest/>`_

`RealPython Testing <https://realpython.com/python-testing/>`_

`Good practises <https://pytest.readthedocs.io/en/2.7.3/goodpractises.html>`_

.. What makes a good tests and best practises.


Code Coverage
-------------

Testing will show us that (hopefully) those bits of code we tested worked as expected, but that is not the whole story. How much of our code has been tested? Having 100% of tests passing is great, but it means nothing if we have not tested all our code. So how do we check it is all being tested? We do this we code coverage.

Coverage.py is capable of doing this very well. There is also a plugin for pytest called pytest-cov, which integrates coverage.py into pytest.  First, install pytest-cov with pip:

```bash
pip install pytest-cov
```

and run it with the command:

```bash
pytest --cov=fibonacci
```

this will produce the same output as when we ran pytest earlier, but it now includes a report on the code coverage like this:

```bash
----------- coverage: platform linux, python 3.7.5-final-0 -----------
Name                         Stmts   Miss Branch BrPart  Cover
--------------------------------------------------------------
src/fibonacci/__init__.py        1      0      0      0   100%
src/fibonacci/fibonacci.py       9      4      4      1    46%
--------------------------------------------------------------
TOTAL                           10      4      4      1    50%
```
 There is quite a bit of information here, but the key things are the filenames in the first column, and their associated coverage percentage in the final column.   We can get a more detailed report, which will tell us which lines of code were not tested, and which were by adding the flag `--cov-report html`.

 ```bash
pytest --cov=fibonacci --cov-report html
```

This will generate a report in html format in a directory called `htmlcov`.  We can view this by opening `htmlcov/index.html` in a web browser.

We can add these options into our `setup.cfg` file so that a coverage report is always generated when we run `python setup.py test` by adding the flag `--cov fibonacci` to `addopts`:

```python
[aliases]
test=pytest

[tool:pytest]
addopts = --verbose
          --cov fibonacci
```
 
We should also update the `tests_require` line in `setup.py` as this now requires `pytest-cov`. `setup.py` should now look like this:

```python
from setuptools import setup, find_packages

setup(
    name="fibonacci",
    version="0.1",
    author="Robin Long",
    author_email="robin.long1@hotmai.co.uk",
    url="https://github.com/longr/python_packaging_example",
    description="A simple package containing a single module with a single function that finds the nth fibonacci number.",
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    install_requires=[""],
    tests_requires=["pytest","pytest-cov"],
)
```

Tests and Continuous Integration
================================

Now that we know how to test our code, we have to remember to do it often. One way to make this easier is to use Continuous Integreation (CI).  The easiest way to do this is by using tools built into by tools such as **github**. As always there are several ways to do this (Github or Gitlab as the provider, and TravisCI, Jenkins, CircleCI or GitLab, to name a few) but we have picked, and will describe one.  Our choice is Github with TravisCI.  When this is configured correctly, everytime you push changes to your Github repository, TravisCI will run your tests and let you know if they pass or not.

Using Continuous Integration has many benefits. Not only is our code tested everytime we push to github, we can test on a variety of python versions and operating systems, without having to have access to a mchine with them - this gives us more confidence in our code, and whether it is reproducible.

To use TravisCI we need to create an account with TravisCI, and grant it access to the repository that conatins your code.  To do this just go to `Travis CI <https://travis-ci.com/>`_ and sign up with your Github account.

.. expand on this

We then need to create a `travis.yml` file in our project directory. Lets create a basic `travis.yml` that will test our code against python 3.6.


```python
dist: xenial

language: python

python:
  - "3.6"

before_install:
  - pip install -U pip
  - pip install -U pytest
  - pip install -U pytest-cov
  
install:
  - pip install '.[test]' . # install our package and test dependencies.

script:
  - pytest
```

Lets look at each part of the file.

* The first line states what operating system we want to use, in this case it is Ubuntu 16.04 (codenamed xenial)

* The `language` statement is the language we wish to use, in our case, python.
* The third line lists what versions of python we want to test against.  We can specificy multiple versisons here, and out tests will be ran against each one. To begin with, we will just use python 3.6, denoted by the '3.6'.

* The `before_install` statement is a list of commands we want to run before our package is installed for testing.
  - `pip install -U pip` will upgrade the currently installed version of pip to the latest. Sometimes errors occur by not having the latest version.
  - ` pip install -U pytest` will install and upgrade pytest.

.. extras_require   https://stackoverflow.com/questions/4734292/specify-where-to-install-tests-require-dependencies-of-a-distribute-setuptools/7747140#7747140

.. tests_require   https://stackoverflow.com/questions/4734292/specify-where-to-install-tests-require-dependencies-of-a-distribute-setuptools/7747140#7747140

    
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




Documenting your project
========================

Use one of any tutorials:

https://www.pythonforthelab.com/blog/documenting-with-sphinx-and-readthedocs/
https://medium.com/@eikonomega/getting-started-with-sphinx-autodoc-part-1-2cebbbca5365
https://gisellezeno.com/tutorials/sphinx-for-python-documentation.html

Location needs to be ../../src for api docs to work.

Discuss:  Use PFTL style or quickstart?  Use make or sphinx-build?  Some errors in layout, look at.

Not looked at doctest yet.








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
   https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html










.. What does what

   setup.py - distributable
   pytest - check it is correct
   coverage.py - check how much is tested
   travis.ci - check it is always checked
   tox/travis.ci - check it is reproducable
   style guide - make sure it is written consistently
   black - force it to be written consistently
   comments - explain why that bit of code does that
   documentation - how to use it
   developer guide - how it works
   contributor guide - how to help
   licence - how it can be used
http://graphviz.org/
https://blog.codinghorror.com/code-tells-you-how-comments-tell-you-why/
