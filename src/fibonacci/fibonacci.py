def fib(n):
    a, b = 0, 1
    fib_number = 1
    if n < 2:
        return n
    while fib_number < n:
        a, b = b, a + b
        fib_number += 1
    return b
