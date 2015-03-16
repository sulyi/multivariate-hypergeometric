#!/usr/bin/env python

"""
Collection of combinatorial functions
and different implementations of them under the hood.
"""

from __future__ import print_function

from math import factorial

__all__ = [ 'nCk', 'nCik', 'LevelLength']


class LevelLength( object ):

    """
    Create an agent to calculates number of all possible Draw on any Level.
    About argument supremum see class Grid.
    At initialization power_set_ordered_by_sums is called, see also there.
    Read length of nth Level by calling precalculate_length, see also there.
    """

    def __init__( self, supremum ):
        self.root = supremum
        self._psobs = self.power_set_ordered_by_sums(supremum)

    @classmethod
    def power_set_ordered_by_sums( cls, base_set ):

        """
        Enumerate sum of elements in each subset by ascending order.
        Source: http://math.stackexchange.com/questions/89419/
        """

        # FIXME: lose ordering input
        n = list( base_set )
        n.sort()

        s = [(0, 0)]
        l = [[]]
        a = [ 0 ] * len(base_set)

        while any( a is not None for a in a):
            min_s = None
            for i, a_ast in enumerate(a):
                if a_ast is not None:
                    curr_s = n[i] + s[a_ast][1]
                else:
                    continue
                if min_s > curr_s or min_s is None:
                    min_s = curr_s
                    i_ast = i
                elif min_s == curr_s and s[a_ast][0] < s[a[i_ast]][0]:
                    i_ast = i
            l_new = list( l[a[i_ast]] )
            l_new.append(( i_ast, n[i_ast] ))
            l.append( l_new )
            s.append(( len(l_new), min_s ))

            a[i_ast] += 1

            # FIXME: lower indexed elements must be lower in value, leading to need of ordering input
            while not all(n[i_ast] >= item and j < i_ast for j, item in l[a[i_ast]]):
                a[i_ast] += 1
                if a[i_ast] == len(s):
                    a[i_ast] = None
                    break
        return s

    def precalculate_length( self, n ):

        """
        Calculate length of nth Level using sum of combinations with replacement.
        """

        members = 0
        collect = 0
        while n >= sum( self._psobs[members] ):
            collect += (-1) ** self._psobs[members][0] * nCik( len(self.root), n - sum(self._psobs[members]) )
            members += 1
        return collect


def nCk( n, k ):
    """Combination n choose k."""
    return _m_nCk( n, k )


def nCik( n, k ):
    """Combination n choose k with replacement."""
    return _m_nCk( n + k - 1, k )


# the hood #


def _f_nCk( n, k ):
    """Factorial formula of binomial coefficient."""
    return factorial( n ) // factorial( k ) // factorial( n - k )


def _m_nCk( n, k ):
    """Multiplicative formula of binomial coefficient."""
    if k > n or k < 0 or n < 0:
        raise ValueError( "Can't choose %d from %d" % ( k, n ) )
    if k > n // 2:
        nk = k
        k = n - k
    else:
        nk = n - k
    b = 1
    for i in range(1, k + 1):
        b *= (nk + i)
        b //= i
    return b


def __r_nCk( n, k ):
    """Recursive formula of binomial coefficient."""
    # recursion is bad, hence it starts: __
    if k == 0 or n == k:
        return 1
    else:
        return __r_nCk(n - 1, k - 1) + __r_nCk(n - 1, k)


if __name__ == '__main__':
    from timeit import timeit

    for function in sorted( dir(), key=lambda name: name[::-1] ):
        if not function.startswith('_', 1) and function.startswith('_'):
            print("%s\n" % function)
            for elements in range(10, 50, 10):
                total = 0
                for choose in range(elements + 1):
                    elapsed_time = timeit("mvhgd.utils.%s(%d,%d)" % (function, elements, choose),
                                          "import mvhgd.utils", number=10000)
                    total += elapsed_time
                    print('(%s, %s) : %s ' % (elements, choose, elapsed_time),end=' ')
                print("\n\ntotal: %f\n" % total)