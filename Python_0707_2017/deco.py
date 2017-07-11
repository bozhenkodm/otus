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
    def wrapped(func):
        return update_wrapper(dec, func)
    return wrapped

# @decorator
def countcalls(func):
    '''Decorator that counts calls made to the function decorated.'''

    # @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


# @decorator
def memo(func):
    '''
    Memorize a function so that it caches all return values for
    faster future lookups.
    '''
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        update_wrapper(wrapper, func)
        return cache[args]
    return wrapper


# @decorator
def n_ary(func):
    '''
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    '''

    @wraps(func)
    def wrapper(*args):
        if len(args) == 1:
            return args[0]
        return reduce(lambda x, y: func(y, x), args[::-1])
    return wrapper


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
    # @decorator
    def dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print '%s --> %s(%s)' % (
                string * wrapper.level, func.__name__,
                ', '.join([str(arg) for arg in args])
            )
            wrapper.level += 1
            result = func(*args, **kwargs)
            wrapper.level -= 1
            print '%s <-- %s(%s) == %s' % (
                string * wrapper.level, func.__name__,
                ', '.join([str(arg) for arg in args]), result
            )
            return result
        wrapper.level = 0
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
    print foo.__name__
    print foo(4, 3)
    print foo(4, 3, 2)
    print foo(4, 3)
    print "foo was called", foo.calls, "times"

    print bar.__name__
    print bar(4, 3)
    print bar(4, 3, 2)
    print bar(4, 3, 2, 1)
    print "bar was called", bar.calls, "times"

    print fib.__doc__
    fib(3)
    print fib.calls, 'calls made'


if __name__ == '__main__':
    main()
