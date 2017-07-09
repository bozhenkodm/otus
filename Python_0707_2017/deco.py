#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import update_wrapper, wraps


def disable(func):
    '''
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    '''
    return func


def decorator(dec):
    '''
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    '''
    def wrapper(*args, **kwargs):
        return dec(*args, **kwargs)
    return update_wrapper(wrapper, dec)


# @decorator
def countcalls(func):
    '''Decorator that counts calls made to the function decorated.'''
    def wrapper(*args, **kwargs):
        wrapper.call_counter += 1
        return func(*args, **kwargs)
    wrapper.call_counter = 0
    return wrapper


@decorator
def memo(func):
    '''
    Memoize a function so that it caches all return values for
    faster future lookups.
    '''
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper


@decorator
def n_ary(func):
    '''
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    '''

    def wrapper(*args):
        reduce(lambda x, y: func(y, x), args[::-1])
    return wrapper


# @decorator
def trace(string):
    '''Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    >>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    '''
    @decorator
    def dec(func):
        def wrapper(level=0, *args, **kwargs):
            print '%s --> %s%s' % (
                string * level, func.__name__, args
            )
            result = func(*args, **kwargs)
            print '%s <-- %s%s == %s' % (
                string * level, func.__name__, args, result
            )
        return wrapper
    return dec


@memo
@countcalls
@n_ary
def foo(a, b):
    return a + b


@countcalls
@memo
@n_ary
def bar(a, b):
    return a * b


@countcalls
@trace("####")
@memo
def fib(n):
    """
    fibbonaci number function
    :param n:
    :return:
    """
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print foo(4, 3)
    print foo(4, 3, 2)
    print foo(4, 3)
    print "foo was called", foo.call_counter, "times"

    print bar(4, 3)
    print bar(4, 3, 2)
    print bar(4, 3, 2, 1)
    print "bar was called", bar.call_counter, "times"

    print fib.__doc__
    fib(3)
    print fib.calls, 'calls made'


if __name__ == '__main__':
    main()
