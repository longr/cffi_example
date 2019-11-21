def fib(n):
    """
    Calculates the value of the nth fibonnaci number.
    
    Function takes a single input, n, the nth fibonacci number, and returns its value.
    
    Parameters
    ----------
     n : int
        nth fibonacci number
    
    Returns
    -------
    int
        The value of the nth fibonacci number.
    
    Examples
    --------
    Get the value of the 10th fibonacci number

    >>> import fibonacci
    >>> fibonacci.fib(10)
    55

    """
    a, b = 0, 1
    fib_number = 1
    if n < 2:
        return n
    while fib_number < n:
        a, b = b, a + b
        fib_number += 1
    return b
