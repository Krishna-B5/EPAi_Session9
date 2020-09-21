import os
import pytest
from session9 import *
from html import escape
from functools import reduce

def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md file missing!"

@smart_divide
def divide(a, b):
    return a/b

def test_smart_divide():
    res, sec, bool1 = divide(2,5)
    if bool1:
        print(res, sec)
    assert bool1 in [True, False]

def test_smart_divide2():
    res, sec, bool1 = divide(5,5)
    if bool1:
        print(res, sec)
    assert bool1 in [True, False]

@logging_func_details
def test_logs():
    msg = divide(2,5)
    assert msg != None, "No Logging details!"

def set_password():
    password = ''
    def inner():
        nonlocal password
        password = '1234'
        return password
    return inner


def test_authenticate():
    current_password = set_password()
    auth_add = authenticate(divide, current_password, 'Secre')
    assert auth_add == 'You scamster!!', 'Hacker is here!!!'

def test_authenticate2():
    current_password = set_password()
    auth_add = authenticate(divide, current_password, '1234')
    assert auth_add[1] == True, 'Hacker is here!!!'

@privilege
def fn(plan):
    return

def test_privilege():
    assert fn('vip') == ['1user', '12months']

def test_privilege2():
    assert fn('vvip') == ['2user', '6months']

def test_privilege3():
    assert fn('premium') == ['2user', '12months']

@singledispatch
def htmlize(a):
    return escape(str(a))

def test_htmlize():
    assert htmlize('1 < 100') == '1 &lt; 100'

def test_htmlize2():
    assert htmlize(100) == '100(<i>0x64</i>)'

def timed(fn, count):
    from time import perf_counter
    from functools import wraps

    @wraps(fn)
    def inner(*args, **kwargs):
        elapsed_total = 0
        elapsed_count = 0

        for i in range(count):
            print(f'Running iteration number {i + 1}')  
            start = perf_counter()
            result = fn(*args, **kwargs)
            end = perf_counter()
            elapsed = end - start
            elapsed_total += elapsed
            elapsed_count += 1

        args_ = [str(a) for a in args]
        kwargs_ = ['{0}={1}'.format(k, v) for k, v in kwargs.items()]
        all_args = args_ + kwargs_
        args_str = ','.join(all_args) 

        elapsed_avg = elapsed_total / elapsed_count

        print(f'{fn.__name__}({args_str}) took {elapsed_avg} seconds')

        return result
    return inner

# @timed
# def fib_reduce(n):
#     initial = (1, 0)
#     dummy = range(n)
#     fib_n = reduce(lambda prev, n: (prev[0] + prev[1], prev[0]), dummy, initial)
#     return fib_n[0]

# fib_reduce = timed(fib_reduce, 15)

# def test_timed():
#     assert fib_reduce(1) == 'Running iteration number 1'