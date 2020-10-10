from random import random
from datetime import datetime


def choose(v: list):
    """ choose one index i of list v with probability v[i]/sum(v)"""
    assert len(v)
    for i in v:
        assert i >= 0   # elements of a distribution must be >= 0!
    s = sum(v)
    assert s > 0    # sum must be greater than 0!

    r = s * random()
    for i in range(len(v)):
        r -= v[i]
        if r <= 0:
            return i


def now_string():
    """datetime.now() -> str"""
    now = str(datetime.now())
    now = now.replace('.', '_')
    now = now.replace(':', '_')
    return now


def argmax(v) -> int:
    index = 0
    best = v[0]
    for i in range(1, len(v)):
        if v[i] > best:
            best = v[i]
            index = i
    return index


def argmin(v) -> int:
    index = 0
    best = v[0]
    for i in range(1, len(v)):
        if v[i] < best:
            best = v[i]
            index = i
    return index


def one_hot(n, length):
    return [1 if i == n else 0 for i in range(length)]


def norm_sum_1(v):
    """sum(v) -> 1"""
    s = sum(v)
    return [i / s for i in v]


def norm_max_1(v):
    """max(v) -> 1"""
    m = max(v)
    return [i / m for i in v]


def add_noise(k):
    """add noise; k=1 means add max(v) to every move, k=0 means no noise"""
    def _add_noise(v):
        m = max(v)
        return [i + abs(k) * m for i in v]
    return _add_noise


def keep_best(v):
    max_ = max(v)
    return [1 if i == max_ else 0 for i in v]


def regularizer(k=.99):
    """
    k = 1.   -> keep best
    k = 0.   -> do nothing
    k = -inf -> random
    """
    if k < 1:
        def regularizer_(v):
            m = max(v) * k
            return [max(0, i - m) for i in v]
        return regularizer_
    else:
        return keep_best


def type_check(*types):
    def _type_check(fun):
        def __type_check(*args, **kwargs):
            out = fun(*args, **kwargs)
            if type(out) not in types:
                message = '\n'
                message += f'\n{fun.__name__}\n'
                if fun.__doc__:
                    message += f'{fun.__doc__}\n'
                message += '\n'
                message += f'expected {" / ".join([str(i) for i in types])}\n'
                message += f'returned {type(out)}\n'
                message += f'\n{out}'
                raise ValueError(message)
            return out
        return __type_check
    return _type_check


def shift_range(length, n):
    for i in range(length):
        yield (i + n) % length


def step(k=1.):
    def f(x):
        return (max(-1., min(+1., x * k))+1)/2
    return f


def shift(v, n):
    """shift array v by n to the right"""
    return [v[(i+n) % len(v)] for i in range(len(v))]


def loop_range(length):
    while True:
        for i in range(length):
            yield i
