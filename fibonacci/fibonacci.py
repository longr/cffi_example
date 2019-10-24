import sys

def fib(n):
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")
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
