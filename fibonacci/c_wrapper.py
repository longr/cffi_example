# import the c extention module we built.
from . import _fibonacci


def cfib(n):
    return _fibonacci.lib.fibonacci(n)


def cfast_fib(n):
    return _fibonacci.lib.fast_fibonacci(n)
