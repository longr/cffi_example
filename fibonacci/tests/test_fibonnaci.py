import pytest
import fibonacci

print("Check fibonacci.fib")


def test_fib_check_zeroth():
    print("1")
    assert fibonacci.fib(0) == 0


def test_fib_check_first():
    print("2")
    assert fibonacci.fib(1) == 1


def test_fib_check_tenth():
    print("3")
    assert fibonacci.fib(10) == 55


print("Check fibonacci.cfib")


def test_cfib_check_zeroth():
    print("4")
    assert fibonacci.cfib(0) == 0


def test_cfib_check_first():
    print("5")
    assert fibonacci.cfib(1) == 1


def test_cfib_check_tenth():
    print("6")
    assert fibonacci.cfib(10) == 55


print("Check fibonacci.fast_fib")

def test_fast_fib_check_zeroth():
    print('7')
    assert fibonacci.fast_fib(0) == 0


def test_fast_fib_check_first():
    print("8")
    assert fibonacci.fast_fib(1) == 1


def test_fast_fib_check_tenth():
    print("9")
    assert fibonacci.fast_fib(10) == 55


print("Check fibonacci.cfast_fib")


def test_cfast_fib_check_zeroth():
    print("10")
    assert fibonacci.cfast_fib(0) == 0


def test_cfast_fib_check_first():
    print("11")
    assert fibonacci.cfast_fib(1) == 1


def test_cfast_fib_check_tenth():
    print("12")
    assert fibonacci.cfast_fib(10) == 55
