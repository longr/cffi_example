[![Build Status](https://travis-ci.org/longr/cffi_example.svg?branch=master)](https://travis-ci.org/longr/cffi_example)
[![codecov](https://codecov.io/gh/longr/cffi_example/branch/master/graph/badge.svg)](https://codecov.io/gh/longr/cffi_example)

# CFFI - Python and C example.

This will mature into something better, but for now it is notes and scriblings as I fumble through running C code in python using cffi.  Links tho pages that have been used to achieve this are listed at the bottom.  Main source of knowledge has been Dimitri Merejkowsky's lets build chuck norris, and the code for this (point) comes from Jim Anderson's contribution on dbader.org


# Creating a python package with external C code.

## Package layout.

In this repository is a sample python package called `fibonacci` that implements 4 methods for calculating the nth fibonacci number.  Two of these are written in pure Python, and two are written in the C language.  Lets first examine the structure of this package.

The package lives in a directory called *fibonacci*, the same name as the package.  Inside this are some files related to testing and installing the package, and another directory of the same name, *fiboncci*.

```
.
|-- fibonacci
|   |-- build_fibonacci.py
|   |-- fibonacci.py
|   |-- c_wrapper.py
|   |-- __init__.py
|   |-- src
|   |   |-- fibonacci.c
|   |   `-- fibonacci.h
|   `-- tests
|       `-- test_fibonnaci.py
|-- MANIFEST.in
|-- notes.md
|-- README.md
|-- requirements.txt
|-- setup.cfg
|-- setup.py
`-- tox.ini

```

Inside the fiboncci directory is the main code for this package.  In it we have four files and two directories.  `__init__.py` tells python that this directory contains a module. `fibonacci.py` contains the two python functions, `c_wrapper.py` contains the python wrappers for the C functions.  `build_fibonacci.py` contains code that compiles the C code.  The `src` directory contains the C headers and files - the C code. The `test` directory contains python code that tests that our package performs as expected.

## Creating the package

To create a simple package with no C code, we just need two files in our `fibonacci` directory: `fibonacci.py` and `__init__.py`.

### __init__.py

`fibonacci/__init__.py` is a special file for python, we know this as its name starts and ends with double underscores. This file tells python that the directory it is in is a module (which can be imported in python doing `import </path/to/directory/><directory_name>`).

The only thing in here is:

```
from .fibonacci import *
from .c_wrapper import *

```

This tells python to look in the package directory (this is done by the `.`) for a file called `fibonacci`, and a file called `c_wrapper`


If we left this empty, we would need to explicitly tell python to import the file `fibonacci.py` and use its functions by doing one of the following:

```
import fibonacci.fibonacci
fibonacci.fibonacci.fib(3)
```
or
```
from fibonacci import fibonacci
fibonacci.fib(3)
```

This would require that any user has to know exactly what the name of each file is that holds each function or variable.

### fibonacci.py

`fibonacci/fibonacci.py` contains our two python functions.  The source code for which is:

```
def fib(n):
    if n < 2:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


def fast_fib(n):
    a, b = 0, 1
    number = 1
    if n < 2:
        return n
    while number < n:
        a, b = b, a + b
        number += 1
    return b
```

As you can see, there is nothing special about this file, it is just a python file with two functions.

### c_wrapper.py

`fibonacci/c_wrapper.py` does what it says, it has python code that we wrap around the C code.  We could have this do something fancy, but these functions simply provide a cleaner and shorter way of calling the functions written in C. It looks like normal python code, which it is.  CFFI (Discussed later) will create a module that we can just import and access the functions of as it it were any normal python module. 

# import the c extention module we built.
from . import _fibonacci


def cfib(n):
    return _fibonacci.lib.fibonacci(n)


def cfast_fib(n):
    return _fibonacci.lib.fast_fibonacci(n)


### build_fibonacci.py

`fibonacci/build_fibonacci.py` is a python file that calls the cffi (C Foreign Function Interface) module.  This is the module that allows us to call C functions from Python.  This is a very short file, and we will explain the contents in more detail later.

```
## CFFI API out-of-line implementation.

import cffi

ffi = cffi.FFI()

# cdef() expects a single string declaring the C types, functions and
# globals needed to use the shared object. It must be in valid C syntax.
# we read in the header file and pass this to cdef.

with open("fibonacci/src/fibonacci.h") as f:
    ffi.cdef(f.read())


# set_source() gives the name of the python extension module to
# produce, and some C source code as a string.
# The C source code needs to make the declared functions,
# types and globals available, so it is often just the "#include".

ffi.set_source(
    "fibonacci._fibonacci",
    '#include "fibonacci.h"',
    include_dirs=["fibonacci/src/"],
    sources=["fibonacci/src/fibonacci.c"],
)

#
ffi.compile(verbose=False)
```

### src

`fibonacci/src` contains the C source code that holds our C functions that we want to call from python, it contains the `.c` file and the header file, `.h`.  `build_fibonacci.py` needs to know about where these files are located, they could be located (almost) anywhere we want, but it makes sense to keep them in their own directory (`src/`), inside the packages directory (`fibonacci/`).

### tests

In this example, `tests` contains a single file, `test_fibonacci.py`. We could easily have many files in here, and it is a good idea to have a different test file for each python file being tested.  These tests will be used by `pytest` to check whether our code gives the results we expect.

##



## Components of module

#. Write module (as in python code)
#. Create module structure.
#. Add setup.py
#. Add tests
#. Add C code.
#. Add CFFI interface.
#. Add travis and CI
#. Add Code coverage.
#. Add docs

## Build and install
Build using
```
python setup.py sdist
```

and then install by doing:

```
pip install . --user
```


## Running.

Run the code using following commands:

```
import Point
new_point = point.Point(2, 3)
new_point.show_point()
```


## How it works.

### Modules / package
Not entirly sure. __init__.py needed so that python knows it is a module. This needs to contain
```
from point import Point
```
otherwise to run the code you need:

```
from point.point import Point
a = Point(2, 3)
```
or
```
import point
point.point.Point()
```

### setup.py

Needed to install packages.  Also calls files to build our c library.

```
from setuptools import setup#, find_packages

setup(name='point',
      version='0.1',
      #packages=find_packages(), #still builds, maynot be needed.
      description='dbader point',
      #py_modules=['point'], ?? What does this do?
      setup_requires=['cffi'],
      cffi_modules=['point/build_point.py:ffi'],
      install_requires=['cffi'],
)
```
name, version, and descrition are obvious.
- TODO: google diff between setup requires and install requires.
```cffi_modules``` is a list of modules for cffi to run for building the c code. Syntax is:
```
<path_to_module>/<build_file>:<name_of_FFI_object_instance)
```
#### py_modules

This is not needed at this level.. Just used for.        #py_modules=['point'], ?? What does this do?
      # explanation here  https://github.com/pypa/packaging.python.org/issues/397


### build_point.py

Should read CFFI docs at https://cffi.readthedocs.org/en/latest/ to explain this file.

create an instance of FFI() (name it that same as we did in the ```cffi_modules``` line of ```setup.py```

```
ffi = cffi.FFI()
```

Then we use ```cdef``` to declare the functions, variables, and so on that we have defined in out c code and want to access from our C extenion.  # https://cffi.readthedocs.org/en/latest/cdef.html#ffi-cdef-declaring-types-and-functions.  These are usually the things in your .h file(s)

Could do this manually as:

```
ffi.cdef(
	"""
	/* Simple structure for ctypes example */
	typedef struct {
	    int x;
	    int y;
	    } Point;

	void show_point(Point point);
	void move_point(Point point);
	void move_point_by_ref(Point *point);
	Point get_default_point(void);
	Point get_point(int x, int y);
	""")
```

If we want all accessible, or don't mind, then we could do:

```
with open("src/point.h") as f:
    ffi.cdef(f.read())
```

which instructs python to read in our point.h and send the contents to ```ffc.cdef```.  This fits better with DRY (Do not Repeat Yourself).

Next we need to tell ```ffi``` about our source files (the .c and associated files.)

```
# set_source is where you specify all the include statements necessary
# for your code to work and also where you specify additional code you
# want compiled up with your extension, e.g. custom C code you've written
#
# set_source takes mostly the same arguments as distutils' Extension, see:
# https://cffi.readthedocs.org/en/latest/cdef.html#ffi-set-source-preparing-out-of-line-modules
# https://docs.python.org/3/distutils/apiref.html#distutils.core.Extension     
ffi.set_source("point._point",
               '#include "point.h"',
               include_dirs=['src/'],
               sources=['src/point.c'],
               extra_compile_args=['--std=c99'])
```

First argument is ***** which is usually the name of the directory containing the python module, followed by a dot, followed by an underscore, and then the name of the c library. ******EXPLAIN******

**** REASON FOR .h?? *********
The next are more obvious, any directories we need to include for it to be able to compile, we put in a list and pass to ```include_dirs```.  Same with source files.

Finally we need to run the compile method on our ```ffi``` object so that is will compile our c library.

```
ffi.compile(verbose=False)
```



### calling the library from python

Next we need to call out module from python. We need a python file that can import this compiled library.  The first thing we need to do in this file is import the our compiled library.

```
import _<library_name>
```

in the case of this example, that is:

```
import _point
```

Then we can access the methods and functions by doing:

```
<imported_module>.lib.<method/function/variable>
```

which again for our case is:

```
_point.lib.get_point(x, y)
```

### Layout
Layout is perhaps optional, but a module layout with module_name, and src is cleaner.

Basic tree is:


```
.---point
|   |--- build_point.py
|   |--- __init__.py
|   \--- point.py
|--- README.md
|--- setup.py
\--- src
     |--- point.c
     \--- point.h
```

NEED TO CHECK THIS.  PEP420 specifys namespace, new layout may be needed.


### Manifest

Need a `MANIFEST.in` and need to specify inclussion of `.h` files.  Need to check the reasoning behind this.


##
Links:
- https://python-packaging.readthedocs.io/en/latest/minimal.html
- https://inventwithpython.com/blog/2019/06/05/pythonic-ways-to-use-dictionaries/
- https://dbader.org/blog/python-cffi
- https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/contributing.html
- https://github.com/jiffyclub/cext23#cffi
- https://dzone.com/articles/executable-package-pip-install
- https://packaging.python.org/tutorials/installing-packages/
- https://realpython.com/python-modules-packages/
- https://dmerej.info/blog/post/chuck-norris-part-5-python-cffi/


## Speed

Four functions are implemented in here, `fib` and `fast_fib` which are pure python functions; and `cfib` and `cfast_fib` which are C functions ran using cffi. There are 2 examples of code here that aim to show: how C code can be called from python, how C code called from python is faster, and how re-writing code can get you faster than the C code (although the c implementation is faster still): `fib` is a slow implementation for finding the nth fibonacci number that uses recursion (and gets slower with higher numbers), and `fast_fib` is a much better way of achiving the same task. Both of these have C implementations. The time taken to run each function is listed below.

```
In [1]: import fibonacci as fib

In [2]: %timeit fib.fib(33)
1 loop, best of 3: 1.37 s per loop

In [3]: %timeit fib.cfib(33)
10 loops, best of 3: 22.5 ms per loop

In [4]: %timeit fib.fast_fib(33)
The slowest run took 12.44 times longer than the fastest. This could mean that an intermediate result is being cached.
100000 loops, best of 3: 2.34 µs per loop

In [5]: %timeit fib.cfast_fib(33)
The slowest run took 63.27 times longer than the fastest. This could mean that an intermediate result is being cached.
1000000 loops, best of 3: 283 ns per loop
```

As we can see, the C implementation `cfib` is 60 times faster than the pure python `fib` function.  Re-writing this slow python function means that `fast_fib` is nearly 10,000 times faster than `cfib`, and is nearly 600,000 times faster than `fib`. `cfast_fib` is then faster still.  This result is highly dependant on the number chosen for `n`, but does show us the power of using C code over pure python code, and the power of well written code over poorly written code.

## Testing

Add details on using pytest.

Tests should be designed so that they test a single function by giving it an input (if needed) and checking that the output is the expected output.  Using `pytest` it is very simple to write tests like this.  First create a file called test_fibonacci.py (by convention all files with tests in should begin test_ ), and put a test in it:

```
def test_fib_check_tenth():
    assert fibonacci.fib(10) == 55
```

This is just a single function that uses the `assert` statement.  All tests should be inside a function, with a function name beginning `test_`.  In this case we are checking that the 10th fibonacci numbe
r is 55.  If it is, then the test will pass - if not it will fail.

We run this test by either, calling pytest by itself, giving it the file name as an argument, or giving it the path to a directory containing tests.  

```
python -m pytest test_fibonacci.py

[longr@localhost cffi_example]$ python -m pytest fibonacci/tests/test_fibonnaci.py 
========================================= test session starts =========================================
platform linux2 -- Python 2.7.16, pytest-4.6.3, py-1.8.0, pluggy-0.12.0 -- /usr/bin/python
cachedir: .pytest_cache
rootdir: /home/longr/Public/PyCFFI/cffi_example, inifile: setup.cfg
collected 1 item                                                                                    

fibonacci/tests/test_fibonnaci.py::test_fib_check_tenth PASSED                                  [100%]

====================================== 1 passed in 0.01 seconds ======================================
```

### Putting tests into a project.

As we are building a module, we will want to tidy things up a little and put them into our package structure.  The best way is to have directory called tests inside each module (remember that a module is a directory containing the file `__init__.py`.

What we also want is to run those tests from setup.py.  To do this we need to add some new lines to setup.py to tell it about our tests.

``
      setup_requires=['cffi','pytest-runner'],
      test_require=['pytest'],
``
First we need to add pytest-runner to the `setup_requires` line as we will use this to run the tests. Then we need to let setup know that our tests will need `pytest` to run.

We now need to create a new file called `setup.cfg` to modify how `setup.py` behaves.

```
[aliases]
test=pytest

[tool:pytest]
addopts = --verbose
```
We specify in here some aliases so that when setup.py wants to run tests, it knows to run pytest instead of the inbuilt test.

Then we specify the command line arguments we wish to pass to pytest, in this case, `--verbose`.

# Questions
- PG 11, namespace and layout. Check how numpy handles this.
- Data files, use pkg_resoucres
- Try and figure out how matplotlib or numpy does its C code.

## To Do.
- Tidy up last few comments and code.
- Write one 'post'?
- Split into multiple?
- Restart a blog?
  - python and cffi.
  - packaging python
  - my hovercraft is full of eels
  - letting go with git.
  Eventually:
  - calling c code from R and Python the easy way.
- Add documentations
- Consider adding a 'case-study' or 'why you should' or 'Alice and Bob story' at the beginning of each tutorial / instruction.

# Links

[Useful links](notes.md)