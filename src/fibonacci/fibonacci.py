"""
main.py
====================================
The core module of my example project

"""

def fib(n):
    """[Summary]
    
    :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
    :type [ParamName]: [ParamType](, optional)
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: [ReturnDescription]
    :rtype: [ReturnType]
    """
    a, b = 0, 1
    fib_number = 1
    if n < 2:
        return n
    while fib_number < n:
        a, b = b, a + b
        fib_number += 1
    return b


"""
Returns the nth fibonacci number.

Takes an integer `n` and returns the nth fibonacci.

Parameters
----------
n : integer
The nth fibonacci number

Returns
-------
b : integer
The value of the nth fibonacci number

"""
