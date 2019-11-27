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


Should we push tox?  Seems problematic and overkill. Not sure I like it.  Needed, realised after tinkering that it is useful and needed.

Then need to look at Docs. Using Sphinx, sphinx-apidoc and doctest - might be others to look at.


Introduction
============

There are lots of resources explaining how to package, test, document and otherwise implement features and styles that will make your python code better and moe sustainable.  However many of these are hidden unless you search for the exact terms, or are not specific enough, or are to specific. These guide hopes to give an opinionated (it won't suggest alternative tools, just pick ones the authors prefer and explain how to use them and only them).   This repositry itself will act as an example of all the features and suggestions.

In the following tutorial we will build a package named `fibonacci` that contains a single function named `fib`.  We shall put this into a package, and then add tests, documentation and take you through the other steps needed to turn our file into a full python package which adhers to all best practises in writing python code and reproducible and sustainable software.

.. contents::

Modules and Packages
===================

.. how to import
.. different way (from X import Y, import X, import X.Y) and how to access modules.
.. redo this with specific test package instead of fictional my_module.
   

.. In python modules are just python, `.py`, files. Packages are collections of modules in a directory with an `__init__.py` file in it.  
.. Could this be written less formally?

In python a module is a single python file ending in `.py` that can be imported using the command `import`. Each module has its own namespace, this means that functions in this module can call each other without having to reference the modules file name. Outside of the module, such as when we import it, the module name needs to be used when calling the a function in the file, such as in the example below.

.. code-block:: python

   >>> import fibonacci
   >>> fibonacci.fib(3)
   2

Here we have imported a module named `my_module` and called a function named `my_function`.

A package is a way of collecting several modules together under another common namespace.

.. code-block:: python

   fibonacci/              # Package
       __init__.py    # Initialisation file
       module_02.py   # Module 2

Here we have a package named `my_package` which contains two modules imaginitivly named `module_01` and `module_02`.  When `my_package` is imported we will need to call the full function name such as `my_package.module_01.function()`.  However functions in each module only need to call the module name followed by the function such as `module_01.function()`.  

.. `RealPython Packages and Modules <https://realpython.com/python-modules-packages/>`_

.. `Packaging - PyPi <https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/contributing.html>`_

.. `Glossary <https://packaging.python.org/glossary/>`_

Package Layout
==============

.. general layout
.. src layout
.. how to import and __init__.py

Packages have a very simple layout.  Each module is inside a directory, the only requirements (other than standard python limits on what can be in a name) is that there must be a file called `__init__.py`. This file can be empty, or it can contain an import statement which imports each module by name. 

There is a lot of flexibility in allowed in how a python package is laid out, and two main schools of thought on how to lay them out.  We recommend using the `src` layout. Here, all python packages are placed inside a directory called `src`. Then later when we get to tests and documentation, they are placed in their respective directories of `tests` and `docs`.  This gives a layout like so:

.. code-block:: bash

   project
   |--docs
   |--src
   |   `--my_package
   |          |-- __init__.py
   |          `-- my_module
   `--tests


This layout will help when it comes to testing later on. For a description of why this layout is better see `Testing and Packaging by Hynek Schlawack <https://hynek.me/articles/testing-packaging/>`_.  For now we shall create our package layout and our files.

First lets create the directory layout

.. code-block:: `bash
		
   mkdir -p fibonacci-project/src/fibonacci

and then create our module file inside `src/fibonacci` which we will call `fibonacci`.

.. code-block:: python

   def fib(n):
       a, b = 0, 1
       fib_number = 1
       if n < 2:
           return n
       while fib_number < n:
           a, b = b, a + b
           fib_number += 1
       return b



we will then need to create an `__init__.py` to turn our directory with a module into a package.  The init file only needs to import our single module.

`__init__.py` file
.. code-block:: python
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

.. code-block:: python
import fibonacci
```

we can then call our function by doing

.. code-block:: python
fibonacci.fibonacci.fib(3)
```

this looks repetative and redundant, as we have two instances of 'fibonacci' in this function call. This is because the first fibonacci is the package (`fibonacci/`) and the second is the module (`fibonacci.py`). Both of these are namespaces used. We can avoid this long function call in a different ways:

We could import the module from the package:

.. code-block:: python
from fibonacci import fibonacii
fibonacci.fib(3)
```

or we could import the module directly

.. code-block:: python
import fibonacci.fibonacci
fibonacci.fib(3)
```


it would be easier for the users of our package if they did not have to do this when importing our package. To avoid this we can change the contents of out `__init__.py` to import functions from our modules into the package which would allow us to call the function like so:

.. code-block:: python
import fibonacci
fibonacci.fib(3)
```

There are two ways to do this. We can import an individual function or we can import the whole of a module. It is far easier to import the whole module, that way we don't have to remember to update `__init__.py` each time we create a new object (recalling that everything, function, classes, and variables are objects in python).  The downide to this is that you then cannot have two functions of the same name in different modules as they will lose their module namespace and only have teh packages namespace. It would also mean that users have access to all objects in our modules, which we may not want.  In which case we can use the second method and import just the function from out module.

to import the whole module out `__init__.py` should look like this:

.. code-block:: python
# import all the objects in the module 'fibonacci'
from .fibonacci import *
```
note that the leading dot is needed (in python 3) to tell python where to begin looking for a module, and the asterix means all.

to only import a single function (which makes little difference in our example as we only have one) we do this:


.. code-block:: python
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

.. how to package
.. setup.py and various layouts.
.. ?should we discuss requirements.txt here or leave until later?

setup.py
--------
.. discuss creating setup.py and import.
.. need to be inside src to do import.
.. discuss types of import and need to rename files.
   
In the current way our package is structured, we have to be in the `src` directory in order to import our package into python. This makes it very hard to distribute or even use our package.  To solve this we will create a `setup.py` file in our project directory which will use the `setuptools` package to allow us to install our package using the package managment system `pip`. 

`setup.py` files can get very complicated in big projects, and if you look at the `setup.py` file for something like numpy, it runs to many lines. Luckily, for small projects we don't need such a complicated file and to create it we essentailly have to just answer a few questions, that hopefully we know as the creator of our package.

Lets look at the `setup.py` file we need for our 'fibonacci' package.

.. code-block:: python
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

.. Should we reintroduce venv here?
   

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

.. code-block:: python
import fibonacci
fibonacci.fib(10)
# 55
```

.. NOTE::
   We will have to rebuild the source distribution, and reinstall it every time we make changes to our package. 

Build and distribute
--------------------

.. again, venv?

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

#
#Manifest
#--------
#
#.. what does manifest protect against?
#
#Licence
#-------
#
#.. Yes needed, add.
#
#Style Guide
#-----------
#
#.. Add these to documentation
#   
#Contributing
#------------
#
#.. Again, documentation
#

Testing with pytest
===================

.. redo with tox, perhaps intorduce with venv for quick turn around.
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

.. code-block:: python
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

# Removed integration with setuptools as this is being depreciated and does not work properly.


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

.. redo with tox

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

Better testing with Tox
=======================

Currently we run our tests by just calling `pytest` on the command line.  If we use virtual enviroments, we can have some increased confidence in our code and tests as we know what package dependencies have been installed.  What happens when we need new packages in our tests, did we document this? What if we want to test against another version of python?  We can do all this with virtual enviroments, but `tox` makes this easier.

Stolen from their own documentation, tox is a generic virtualenv management and test command line tool you can use for:

- checking your package installs correctly with different Python versions and interpreters
- running your tests in each of the environments, configuring your test tool of choice
- acting as a frontend to Continuous Integration servers, greatly reducing boilerplate and merging CI and shell-based testing.

All of this makes tox a great tool and key one to use.

Configuring Tox
---------------

After some initialisation, tox will make running our tests easier and simpler.  Firstly we need to install tox, with pip the command is:

.. code-block:: bash

   pip install tox

   
Then we need to put information about our project into a file called `tox.ini`, this tells tox which tests we want to run, and which versisons of python to run those tests against.

.. code-block:: python

   # tox.ini
		
   [tox]
   envlist = py27, py35, py36, py37, py38

   [testenv]
   deps = -r{toxinidir}/requirements_test.txt
     
   commands = pytest

Lets look at this file in detail.  First we have `[tox]` which will contain the global options we want to configure for tox.  The only option we have specified here is `envlist`, and we have listed five versions of python we wish to test against. Notice that these are abbreviated to **py** and the major and minor version numbers without a decimal point; as such python 3.6 becomes py36.

The next section, `[testenv]`, specifies the options we want in our test environment. Tox will install our package inside the virtual environment, and will pickup the dependencies from `setup.py`; however, `setup.py`, does not contain information on the dependencies for our test environment, so we need to speciy these separatly.  Using the DRY (Don't Repeat Yourself), the best way to specify this is using a requirements file to list the dependencies for running our tests.  We shall use a file called `requirements_test.txt` to list our depdencies. This file will contain each dependency on a separate line and should look like this for our package:

.. code-block:: python

   pytest
   pytest-cov

This file should be located in our packages root file (where our setup.py file is located).  We can then tell tox about it by using `-r{toxinidir}/requirments_test.txt`. `{toxinidir}` is a tox variable which evalulates to the directory that the `tox.ini` file is located in (this is useful to ensure paths are correct).  Also note the lack of a space between `-r` and `{toxinidir}/requirements_test.txt`.
   
The final part of the `tox.ini` file is the `commands` line, here we need to specify the command we wish to use to run our tests, in this case it is `pytest`.

Running Tox
-----------

We can run our tests by calling `tox` on the command line:

.. code-block:: bash

   $ tox
   ...
   py38 inst-nodeps: /home/longr/Public/PyCFFI/python_packaging_example/.tox/.tmp/package/1/fibonacci-0.1.zip
   py38 installed: attrs==19.3.0,coverage==4.5.4,fibonacci==0.1,more-itertools==7.2.0,packaging==19.2,pluggy==0.13.1,py==1.8.0,pyparsing==2.4.5,pytest==5.3.0,pytest-cov==2.8.1,six==1.13.0,wcwidth==0.1.7
   py38 run-test-pre: PYTHONHASHSEED='545188176'
   py38 run-test: commands[0] | pytest
   =============================== test session starts ==================================
   platform linux -- Python 3.8.0, pytest-5.3.0, py-1.8.0, pluggy-0.13.1
   cachedir: .tox/py38/.pytest_cache
   rootdir: /home/longr/Public/PyCFFI/python_packaging_example
   plugins: cov-2.8.1
   collected 3 items
   
   tests/test_fibonacci.py ...                                                     [100%]

   ============================== 3 passed in 0.03s =====================================
   ___________________________________ summary __________________________________________
   py27: commands succeeded
   py36: commands succeeded
   py37: commands succeeded
   py38: commands succeeded
   congratulations :)

tox runs the tests we wrote for each of the versions of python specified in our `tox.ini`; Note that in the above output, we have truncated the output and shown the tests being run against the last version of python only.

.. warning::

   You may get errors when trying to run this on your own system.  This will because the various implementations are python will not be installed. By default only one version of python3 is installed.  To solve this we can ask tox to run against a single implementation by calling `tox -e <python_enviroment>`.  To run only python 3.7 we would call `tox -e py37`.

   
Tox and Code coverage
---------------------

.. https://pytest-cov.readthedocs.io/en/latest/tox.html

Previously we used code coverage with pytest to see how much of our code has been covered by tests.  We can do this in tox aswell by adding the `--cov fibonacci` flag to `command = pytest` line in our tox.ini.

One common problem people run into with pytest and tox is that `pytest-cov` will erase previous coverage data by default.  This is unwanted with `tox` as we want the combined coverage for multiple version (especially if we have lines of code that are only ran under certain versions).  To get the combined coverage we need to use `--cov-append`. As this will then keep the coverage data we need tox to clean up between runs, we can do this by creating a `[testenv:clean]` option and adding it to out `envlist`:


..ignore the concept of parrallel, but see //pytest-cov.readthedocs.io/en/latest/tox.html if we plan to.

.. code-block::

   # tox.ini
		
   [tox]
   envlist = clean, py27, py35, py36, py37, py38

   [testenv]
   deps = -r{toxinidir}/requirements_test.txt
   commands = pytest --cov fibonnaci

   [testenv:clean]
   deps = coverage
   skip_install = true
   commands = coverage erase

We can now run tox again and it will print out our coverage:

.. code-block:: bash

   $ tox
   ...
   
   ----------- coverage: platform linux, python 3.8.0-final-0 -----------
   Name                                                           Stmts   Miss  Cover
   ----------------------------------------------------------------------------------
   .tox/py27/lib/python2.7/site-packages/fibonacci/__init__.py        1      0   100%
   .tox/py27/lib/python2.7/site-packages/fibonacci/fibonacci.py       9      0   100%
   .tox/py36/lib/python3.6/site-packages/fibonacci/__init__.py        1      0   100%
   .tox/py36/lib/python3.6/site-packages/fibonacci/fibonacci.py       9      0   100%
   .tox/py37/lib/python3.7/site-packages/fibonacci/__init__.py        1      0   100%
   .tox/py37/lib/python3.7/site-packages/fibonacci/fibonacci.py       9      0   100%
   .tox/py38/lib/python3.8/site-packages/fibonacci/__init__.py        1      0   100%
   .tox/py38/lib/python3.8/site-packages/fibonacci/fibonacci.py       9      0   100%
   ----------------------------------------------------------------------------------
   TOTAL                                                             40      0   100%
   
   
   ================================ 3 passed in 0.09s ================================
   ______________________________________ summary ____________________________________
    clean: commands succeeded
    py27: commands succeeded
    py36: commands succeeded
    py37: commands succeeded
    py38: commands succeeded
    congratulations :)

The output above is truncated, but we can see that the list of files covered by the tests increase with each run as more files (in different virtual environments) are added to the coverage report.  You only need to have 100% coverage across all files, not in each one, to get 100% coverage.
   

   Tests and Continuous Integration
================================

.. redo with tox

We now have a python package that is installable, and has inbuilt tests and coverage reports - the later help build confidence in the packages reproducibility. We can ensure these tests are ran when we push our commits to github, this will give us confidence that our public code has always been tested, and show other users that its has been tested as well.

We ensure that these tests are ran through Continuous Integration (CI), whereby each time we push a commit to github, it triggers scripts to be ran against the code, or through something called webhooks, triggers external services to run scripts against our repository.

We will look first at **TravisCI** which will use tox to test our code, and then codecov.io which will generate and host pretty code coverage reports for our code.

TravisCI
--------


To use TravisCI we need to create an account with TravisCI, and grant it access to the repository that conatins your code.  To do this just go to `Travis CI <https://travis-ci.com/>`_ and sign up with your Github account.

.. Add setting up travis on github and getting account

TravisCI provides virtual machines that our package is built and ran on, this allows us to test against multiple versions of python, and against different operating systems.  We will also use an extra package called `tox-travis` which makes it easier to use tox and travis together.

We specify what we want travis to run using the file `.travis.yml`:

.. code-block:: python

   language: python

   python:
     - "2.7"
     - "3.5"
     - "3.6"
     - "3.7"
     - "3.8"

   install:
     - pip install tox-travis

   script:
     - tox -vv

There are quite a few things specified here so lets look at them one at a time.

`language: python` specifies the programming language we will be using.

`python:` is a list of the python versions we want to run against.

`install:` is a list of things we need installing before we can run.  As our package dependencies and test dependencies are already in `setup.py` and `tox.ini` we only need to specify one extra package which is tox-travis.  tox-travis is a package that makes running tox and travis together a little simpler and removes the need to type as much in the `.travis.yml` file.

`script:` is a list of commands and scripts to run for each version of python.  In our case we just want to run tox; the `-vv` is enabling extra verbosity from tox, just incase we have errors.

Now, each time we issue a `git push` and our commits are sent to github, these test will be ran.  We can tell everyone about how our tests are being passed by adding a badge to our README.md. The code we will need to add to our README.md will look similar to this:

.. code-block::

   [![Build Status](https://travis-ci.org/longr/cffi_example.svg?branch=master)](https://travis-ci.org/longr/cffi_example)

You can get the badge for your package by going to:

.. Add instructions on getting badge.

.. extras_require   https://stackoverflow.com/questions/4734292/specify-where-to-install-tests-require-dependencies-of-a-distribute-setuptools/7747140#7747140

.. tests_require   https://stackoverflow.com/questions/4734292/specify-where-to-install-tests-require-dependencies-of-a-distribute-setuptools/7747140#7747140

    
`Extensive Python Testing on Travis CI <https://blog.travis-ci.com/2019-08-07-extensive-python-testing-on-travis-ci>`_

`Untold stories about python unit tests <https://hackernoon.com/untold-stories-about-python-unit-tests-a141501f0ee>`_

Test coverage
=============

Now that we have tests working with continuous integration we can expand this to code coverage.  The first thing we need to do is signup for an account on `Codecov <https://codecov.io/>`_ which just requires us to log in with our GitHub account.  Then we have to add the relevant lines to our `.travis.yml` so that it looks like this:

.. code-block:: python

   language: python

   python:
     - "2.7"
     - "3.5"
     - "3.6"
     - "3.7"
     - "3.8"

   install:
     - pip install tox-travis codecov

   script:
     - tox -vv

   after_success:
     - codecov

We have now added `codecov` as a dependency under `install:`, and a new section labelled `after_success`:`; this section contains the commands to run once all our `script:` jobs have been run successfully. We have added one entry, `codecov`.  As long as we have a public GitHub account, and a codecov.io account, this will send our coverage report to codecov.io.

       
`Pytest and coverage <https://stackoverflow.com/questions/21991765/how-to-generate-coverage-from-setup-py>`_

`pytest import issues <http://doc.pytest.org/en/latest/pythonpath.html#pytest-vs-python-m-pytest>`_

`Codecov + python + travis <https://dev.to/j0nimost/using-codecov-with-travis-ci-pytest-cov-1dfj>`_
`exclude files from codecov <https://docs.codecov.io/docs/codecov-yaml>`_
`Codecov + python + travis beginners <https://medium.com/datadriveninvestor/beginners-guide-to-using-codecov-with-python-and-travis-ci-c17659bb711>`_
`Codecov yaml <https://docs.codecov.io/docs/codecov-yaml>`_


.. Testing on multiple OS's

`Testing Your Project on Multiple Operating Systems <https://docs.travis-ci.com/user/multi-os/>`_

`Windows build on Travis <https://docs.travis-ci.com/user/reference/windows/>`_

Documentation
=============

.. Add description of how to document and different types

.. https://realpython.com/documenting-python-code/

One of the main tasks we need to do for our project, and the most over looked is to document it.  As usual, there are many ways to do this, but only one that we will look at.  We will use a python program called **sphinx**, which converts reStructuredText (.rst) files into our choice of html, pdf, and epub.  We can choose to do all or some of these.

The first things we need to do is create a directory to store our documentation in, by convention this should be called `docs`. We then need to `cd` into this directory and set it up.

.. code-block:: bash

   $ mkdir docs
   $ cd docs

We will need to install sphinx before we can go any further with setting up our documentation. We do this using pip:

.. code-block:: bash

   $ pip install sphinx

Then we can setup our documentation. Sphinx needs a configuration file named `conf.py` and a few additional files for building the documentation.  We can generate all of these using a command called `sphinx-quickstart`. There are two ways to do this, and both result in the same setup. We can run the command by itself and it will ask us questions that we need to enter; some of these need specific answers, and for others we can use the default options. To do this, just type `sphinx-quickstart` from inside the `docs` directory, and accept the default answers (by pressing *enter*) except for the following (answers in bold):

* `Separate source and build directories (y/n) [n]:` **y**
* `Project name:` Enter the name of the project, this should be the same name as we used for our package, in this case **fibonacci**.
* `Author name(s):` This wants to be the author(s) names, for me that is 'Robin Long'
* `Project release`: This is the current version of the project, 0.1 for example.
* `Project language`: This is what language the project is in, the default in **en** (english)
* `Source file suffix [.rst]`: This is the file extention for any files we want included in our documentation, the default (**rst**) is correct.
* `Name of your master document (without suffix) [index]`: Accept the default here, this is the name of main file that all others will be linked from.

There will be a series of questions now, where the default answer will be no, it is fine to just accept these.

* `Create Makefile? (y/n) [y]`: This will create a Makefile making it easier to build the documentation, the default **y** is correct.
* `Create Windows command file? (y/n) [y]`: This is the same, but for windows, accepting the default is fine.

This should create a directory stucture that looks like this:

.. code-block:: bash

   docs/
   ├── build
   ├── conf.bk
   ├── make.bat
   ├── Makefile
   └── source
       ├── conf.py
       ├── index.rst
       ├── _static
       └── _templates

.. NOTE::
   If you want to avoid going through all those prompts, the same can be achieved with a long command line. Remember to replace project name (`-p`), author (`-a`), release (`-r`) and version (`-v`). If needed also replace language (`-l`). 
   `sphinx-quickstart -p 'fibonacci'  -a 'Robin Long' -v '0.1' -r '0.1' --makefile -q --sep -l en
     
Before we go any further we should make some changes to the default configuration file, `source/conf.py`.  We need to uncomment the following lines:

.. code-block:: python

   #import os
   #import sys
   #sys.path.insert(0, os.path.abspath('.'))

and add in the correct path to our python module so that is now reads:

.. code-block:: python
		
   import os
   import sys
   sys.path.insert(0, os.path.abspath('../../src/'))


.. NOTE::
   The path `../../src` is a relative path from the `conf.py` file is, which should be `<root_project_dir>/docs/source/`; to where our package is which should be `<root_project_dir>/src`.

The next thing we need to do (which is encouraged, but optional) is change the theme to one that is a lot nicer. Just find the line beginning `html_theme` and change it from:

.. code-block:: python

   html_theme = 'alabaster'

to

.. code-block:: python

   html_theme = 'sphinx_rtd_theme'

Using this theme will require an extra package to be installed. From within our virtual environment we do:

.. code-block:: bash

   $ pip install sphinx_rtd_theme

   
   
Building the documentation
--------------------------

Now that we have setup the documentation we want to test it compiles and build it.  We can do this using the make file. There are several options that we can pass to the make file depending upon what output we would like, generally we will want the output to be a webpage, a pdf file, or an epub file.  We can build these by passing the relevant option. To build the documentation as a webpage, from our root project directory, do the following:

.. code-block:: bash

   $ make -C docs html

`-C docs` tells `make` to change to the `docs` directory before building and `html` tells it we want to build a webpage as the output. The webpage will be built in `docs/build/html`. We can view the page by opening `docs/build/html/index.html`.  On linux this is done on the command line using one of the following:

.. code-block:: bash

   $ # Google Chrome
   $ google-chrome docs/build/html/index.html
   $ # Firefox
   $ firefox docs/build/html/index.html

It would be better, if like the testing, we build our documentation in a virtual enviroment so that when we distribute our package it will be clear how to build, and we can be sure it works.

First lets edit `setup.py` to let it know what dependencies we need for building the documentation:

* We need to add a list containing the required packages.
* Add a key value pair to `extras_requires` linking the packages to a name.

Our `setup.py` should now look like this (some lines ommitted)

.. code-block:: python
		:empasize-lies: 13,14,15,29
   #!/usr/bin/env python
   # -*- coding: utf-8 -*-

   from setuptools import setup, find_packages

   install_requires = []

   tests_require = [
       'pytest',
       'pytest-cov',
   ]

   docs_require = [
       'sphinx',
       'sphinx_rtd_theme',
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
       extras_require={'testing': tests_require,
		       'docs': docs_require,},
   )

.. NOTE::
   Adding key-value pairs to `extras_requires` means that we have optional packages that can be installed using pip by calling `pip install package[optional]`, for our package, `fibonacci`, this would be `pip install fibonacci[docs]`.

Now that we have added the dependencies needed for our documentation to `setup.py` we can add an entry in tox to build the docs in a virtual enviroment. We just need to add these extra configurations to the end of our tox.ini file:

.. code-block:: python

   [testenv:docs]
   basepython = python3
   whitelist_externals = make
   extras =
       docs
   commands =
       make -C docs html "SPHINXOPTS=-W -E"

This is similar to what we have before. The firstline, `basepython = python3` insturcts tox to build the documentation under python3 (instead of python2). For any external command (outside of python) that we wish to use we need to whitelist it; we do this as `whitelist_externals = make`. The next two are similar to what we have seen before: **extras** is the key from `setup.py`; **commands** is the command needed to build the documentation that we used previously. The main difference is that we have added `"SPHINXOPTS=-W -E". These pass extra flags to the sphinx-build command. `-W` turns warnings into errors, this prevents us building when we have warnings. `-E` forces sphinx to re-read all files for each build.

We can now build our documentation with tox:

.. code-block:: bash

   tox -e docs

We can add more options to tox for the different kinds of documentation we want to produce. We just need to change the env name (the text after `testenv:`) and the output type for sphinx.  Here is pdf and epub (note, pdf requires latex to be installed).

.. code-block:: python

   [testenv:pdf]
   basepython = python3
   whitelist_externals = make
   extras =
       docs
   commands =
       make -C docs pdflatex "SPHINXOPTS=-W -E"

   [testenv:epub]
   basepython = python3
   whitelist_externals = make
   extras =
       docs
   commands =
       make -C docs epub "SPHINXOPTS=-W -E"

If we wished, we could build all in one go with:

.. code-block:: python

   [testenv:pdf]
   basepython = python3
   whitelist_externals = make
   extras =
       docs
   commands =
       make -C docs pdflatex html epub "SPHINXOPTS=-W -E"

   
Writing Documentation in Sphinx
-------------------------------

We can now create our documentation.  Everything should be written in `.rst` files in `docs/source/`.

.. Add reST primer.

.. Discuss types of documenation?
.. https://brandons-sphinx-tutorial.readthedocs.io/en/latest/quick-sphinx.html

Automatic Documentation
-----------------------

Sphinx also has very helpful plugins that allow us to automatically generate API, documentation for the docstrings in our code. This means that users will be able to quickly access information on the functions contained with in our code and how to use them.

To use this, we need to tell sphinx which extentions to use. We can do this by editting the following line in `docs/source/conf.py` to look like this:

.. code-block:: python

   extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

* `sphinx.ext.autodoc` is the extention that will build the API documentation
* `sphinx.ext.napoleon` enables autodoc to understand numpy style doc strings which are easier to read.

Whilst we said the documentation is generated automatically we do need to do a little work; we have to tell sphinx which modules to automatically document. We do this be creating a file called `docs/source/fibonacci.rst` (named after our package) with the following lines in it:

.. code-block:: python

   .. automodule:: fibonacci.fibonacci
      :members:

We then need to link to this from `index.rst`. The simplest way is to put it into the contents of `index.rst`. Edit `index.rst` so that the contents now shows:

.. code-block:: rest

   .. toctree::
      :maxdepth: 2
      :caption: Contents:
      
      fibonacci

Be very careful about the indentation. We call the file by its name without `.rst` on the end, but we must ensure its indent is correct.

Now when we use the `make` command, or more correctly use `tox -e docs` to build our documentation it will build the API documentation as well.

.. INFORMATION::
   As our project progress it might make sense to split this into more files; perhaps one called `modules.rst` which links to all the others with one `.rst` file per module/sub-module.

.. which first User, or guide?  Guide as depends on user.


Testing documentation with Doctest
----------------------------------

.. Should we do pytest --doctest-modules??  http://doc.pytest.org/en/latest/doctest.html


   
Documenting your project
========================

Use one of any tutorials:

https://www.pythonforthelab.com/blog/documenting-with-sphinx-and-readthedocs/
https://medium.com/@eikonomega/getting-started-with-sphinx-autodoc-part-1-2cebbbca5365
https://gisellezeno.com/tutorials/sphinx-for-python-documentation.html

Location needs to be ../../src for api docs to work.

Discuss:  Use PFTL style or quickstart?  Use make or sphinx-build?  Some errors in layout, look at.

Not looked at doctest yet.

for apidocs:  https://github.com/sphinx-contrib/apidoc

Main note on docs is need to add modules.rst to index.rst or somewhere so it is linked.  Have put notes in tox and how to use tox for api gen and docs gen.  Look at testing next, and then deploying.


.. links
   https://opendev.org/openstack/openstacksdk/src/branch/master/tox.ini
   https://pypi.org/project/pytest-sphinx/
   https://samnicholls.net/2016/06/15/how-to-sphinx-readthedocs/
   https://tox.readthedocs.io/en/latest/example/documentation.html

   https://medium.com/@eikonomega/getting-started-with-sphinx-autodoc-part-1-2cebbbca5365
   https://alexgaynor.net/2010/dec/17/getting-most-out-tox/
   https://github.com/Syntaf/travis-sphinx
   https://ofosos.org/2019/01/06/doctest-travis/
   https://blog.justinwflory.com/2018/12/meet-an-opinionated-quickstart-for-sphinx-docs-authors/
   https://docs.pylonsproject.org/projects/docs-style-guide/
   https://github.com/Pylons/docs-style-guide/blob/master/tox.ini

   ## works  builds docs into .tox area. Better?
#[testenv:docs2]
#description = invoke sphinx-build to build the HTML docs
#basepython = python3.7
#deps = sphinx >= 1.7.5, < 2
#     sphinx_rtd_theme
#commands = sphinx-apidoc -f -o docs/source/ src/fibonacci
#	 sphinx-build -d "{toxworkdir}/docs_doctree" docs/source "{toxworkdir}/docs/build" --color -W -bhtml {posargs}
#           python -c 'import pathlib; print("documentation available under file://\{0\}".format(pathlib.Path(r"{toxworkdir}") / "docs_out" / "index.html"))'
# not sure what last line does

#works
#works with apidoc
### Stolen from https://opendev.org/openstack/openstacksdk/src/branch/master/tox.ini
#[testenv:docs]
#deps =
#    sphinx
#    sphinx_rtd_theme
#commands =
#    sphinx-apidoc -f -o docs/source/ src/fibonacci
#    sphinx-build -W -d docs/build/doctrees -b html docs/source/ docs/build/html
#    python -m sphinx -b doctest -d {envdir}/.cache/doctrees docs/source {envdir}/.cache/doctest
#


# Could  use

#https://github.com/Pylons/docs-style-guide/blob/master/tox.ini
#https://github.com/iScrE4m/pyCardDeck/blob/master/tox.ini

# https://developer.ridgerun.com/wiki/index.php/How_to_generate_sphinx_documentation_for_python_code_running_in_an_embedded_system
#[testenv:html]
#basepython = python3.6
#whitelist_externals = make
#commands =
#    make -C docs html BUILDDIR={envdir} "SPHINXOPTS=-W -E"

# make -C dir: change to dir first.

# Also look at:
# https://tox.readthedocs.io/en/latest/example/documentation.html
# https://alexgaynor.net/2010/dec/17/getting-most-out-tox/
# https://stackoverflow.com/questions/56336234/build-fail-sphinx-error-contents-rst-not-found
# https://www.dominicrodger.com/2013/07/26/tox-and-travis/
# https://github.com/tox-dev/tox-travis/blob/master/.travis.yml
# 

.. LOOK at this: https://github.com/Pylons/pyramid/blob/master/docs/Makefile

Pyramids is gold standard for sphinx.  They have modifed make file, consider doing the same to allow build.    Also perhaps remove travis-tox?? to confusing and hides things?

CI and Docs
===========

Read the docs
-------------

Code Quality with Linters
=========================

`Black - code style <https://github.com/python/black>`_
 Use flag `--skip-string-normalization` as black swaps to double which is harder to read.

Uploading to PiPy with CI
=========================

`Upload to PyPi <https://gist.github.com/gboeing/dcfaf5e13fad16fc500717a3a324ec17>`_


.. Do we need to talk about MANINFEST.ini and packaging data with projects?

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
