from time import gmtime, strftime
import time
from operator import itemgetter 
from html import escape
from functools import wraps

def smart_divide(func):
    def inner(a, b):
        time_sec = int(strftime("%S", gmtime())) 
        if time_sec % 2 != 0:
            # print(f"Odd Second {time_sec}")
            return func(a, b), {time_sec}, True
        else:
            return func(a, b), {time_sec}, False
    return inner

def logging_func_details(fn):
    cnt = 0
    def inner(*args, **kwargs):
        nonlocal cnt
        cnt += 1
        time_detail = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
        msg = (f'{fn.__name__} method has been called {cnt} times accessed at {time_detail} with arguments {args}')
        return fn(*args, **kwargs), msg
    return inner

def authenticate(fn, current_password, user_password):
    cnt = 0
    if user_password == current_password():
        def inner(*args, **kwargs):
            nonlocal cnt
            cnt += 1
            print(f'{fn.__name__} was called {cnt} times')
            return fn(*args, **kwargs)
        return inner, True
    else:
        return 'You scamster!!'

def privilege(fn):
    '''
    fn -> function name add, mul, div
    my_dict -> param dict
    return -> dict for each method names div, mul, add
    '''
    cnt = 0
    plans = ['1user', '2user','6months', '12months']
    def inner(customer):
        nonlocal cnt, plans
        if customer == 'basic':
            index_list = [0,2]
            return list(itemgetter(*index_list)(plans)) 
        elif customer == 'vip':
            index_list = [0,3]
            return list(itemgetter(*index_list)(plans)) 
        elif customer == 'vvip':
            index_list = [1,2]
            return list(itemgetter(*index_list)(plans)) 
        elif customer == 'premium':
            index_list = [1,3]
            return list(itemgetter(*index_list)(plans)) 
    return inner

def singledispatch(fn):
    registry = {}
    registry[object] = fn
    registry[int] = lambda a: f'{a}(<i>{str(hex(a))}</i>)'
    registry[str] = lambda s: escape(s).replace('\n', '<br/>\n')

    def inner(arg):
        return registry.get(type(arg), registry[object])(arg)
    return inner