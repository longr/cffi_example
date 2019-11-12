import pytest
import fibonacci

def test_fib_check_zero():
    assert fibonacci.fib(0) == 0

def test_fib_check_one():
    assert fibonacci.fib(1) == 1

def test_fib_check_ten():
    assert fibonacci.fib(10) == 55
