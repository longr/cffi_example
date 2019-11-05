import pytest
import fibonacci

def test_fib_check_zero():
    assert fibonacci.fib(0) == 0
