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
