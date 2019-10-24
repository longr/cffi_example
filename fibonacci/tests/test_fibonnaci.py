import pytest
import fibonacci

def test_fib_check_zeroth():
    assert fibonacci.fib(0) == 0

   
def test_fib_check_first():
    assert fibonacci.fib(1) == 1

   
def test_fib_check_tenth():
    assert fibonacci.fib(10) == 55


def test_cfib_check_zeroth():
    assert fibonacci.cfib(0) == 0


def test_cfib_check_first():
    assert fibonacci.cfib(1) == 1


def test_cfib_check_tenth():
    assert fibonacci.cfib(10) == 55


def test_fast_fib_check_zeroth():
    assert fibonacci.fast_fib(0) == 0


def test_fast_fib_check_first():
    assert fibonacci.fast_fib(1) == 1


def test_fast_fib_check_tenth():
    assert fibonacci.fast_fib(10) == 55

    
def test_cfast_fib_check_zeroth():
    assert fibonacci.cfast_fib(0) == 0


def test_cfast_fib_check_first():
    assert fibonacci.cfast_fib(1) == 1


def test_cfast_fib_check_tenth():
    assert fibonacci.cfast_fib(10) == 55
