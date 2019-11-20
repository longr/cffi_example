def fib(n):
    """
    Summary line.
    
    Extended description of function.
    
    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2
    
    Returns
    -------
    int
        Description of return value
    
    """
    a, b = 0, 1
    fib_number = 1
    if n < 2:
        return n
    while fib_number < n:
        a, b = b, a + b
        fib_number += 1
    return b
