#/usr/bin/env python

"""
a collection of combinatorial functions
and different implementations of them under the hood
"""

from math import factorial

__all__ = [ 'nCk', 'nCik' ]

# TODO: revert pre_calculate_length into utils


def nCik( n, k ):
    """n choose k"""
    return _f_nCik( n, k )


def nCk( n, k ):
    """n choose k with replacement"""
    return _f_nCk( n, k )

#### the hood ####


def _f_nCk( n, k ):
    if k > n / 2:
            k = n - k
    return factorial( n ) / factorial( k ) / factorial( n - k )


def _f_nCik( n, k ):
    if k > n - 1:
        k = n - k
    return factorial( n + k - 1 ) / factorial( k ) / factorial( n - 1 )


def _m_nCk( n, k ):
    if k > n / 2:
            k = n - k
    return reduce(lambda y, x: y * (n - k + x) / x, range(1, k + 1), 1)


def _m_nCik( n, k ):
    if k > n - 1:
        k = n - k
    return reduce(lambda y, i: y * (n - 1 + i) / i, range(1, k + 1), 1)


if __name__ == '__main__':
    from timeit import timeit
    for f in sorted( dir(), key=lambda s: s[::-1] ):
        if not f.startswith('_', 1) and f.startswith('_'):
            print f
            for i in range(10, 50, 10):
                print (i, i/2), ':', timeit("mvhgd.utils.%s(%d,%d)" % (f, i, i/2), "import mvhgd.utils", number=100000),
            print
