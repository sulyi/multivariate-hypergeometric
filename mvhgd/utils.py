#/usr/bin/env python

"""
a collection of combinatorial functions
and different implementations of them under the hood
"""

from math import factorial

__all__ = [ 'nCk', 'nCik', 'Dosage' ]


class Dosage( object ):
    """
    """
    # TODO: doc, Dosage

    def __init__( self, grid ):
        self.patient = grid
        self._psobs = self._power_set_ordered_by_sums

    @property
    def _power_set_ordered_by_sums( self ):

        """
        """
        # TODO: doc, _power_set_ordered_by_sums, http://math.stackexchange.com/questions/89419/

        # FIXME: lose ordering input
        n = list( self.patient.root )
        n.sort()

        s = [(0, 0)]
        l = [[]]
        a = [ 0 ] * self.patient.m

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

            # FIXME: lover indexed elements must be lover in value, leading to need of ordering input
            while not all(n[i_ast] >= item and j < i_ast for j, item in l[a[i_ast]]):
                a[i_ast] += 1
                if a[i_ast] == len(s):
                    a[i_ast] = None
                    break
        return s

    def precalculate_length( self, n ):

        """
        """
        #TODO: doc, calculate length

        members = 0
        collect = 0
        while n >= sum( self._psobs[members] ):
            collect += (-1) ** self._psobs[members][0] * nCik( self.patient.m, n - sum(self._psobs[members]) )
            members += 1
        return collect


def nCk( n, k ):
    """n choose k"""
    return _m_nCk( n, k )


def nCik( n, k ):
    """n choose k with replacement"""
    return _m_nCk( n + k - 1, k )

#### the hood ####


def _f_nCk( n, k ):
    """factorial formula of binomial coefficient"""
    return factorial( n ) / factorial( k ) / factorial( n - k )


def _m_nCk( n, k ):
    """multiplicative formula of binomial coefficient"""
    if k > n or k < 0 or n < 0:
        raise ValueError( "Can't choose %d from %d" % ( k, n ) )
    if k > n / 2:
        nk = k
        k = n - k
    else:
        nk = n - k
    return reduce(lambda y, x: y * ( nk + x) / x, range(1, k + 1), 1)


if __name__ == '__main__':
    from timeit import timeit
    for function in sorted( dir(), key=lambda name: name[::-1] ):
        if not function.startswith('_', 1) and function.startswith('_'):
            print "%s\n" % function
            for elements in range(10, 50, 10):
                total = 0
                for choose in range(elements + 1):
                    elapsed_time = timeit("mvhgd.utils.%s(%d,%d)" % (function, elements, choose),
                                          "import mvhgd.utils", number=10000)
                    total += elapsed_time
                    print (elements, choose), ':', elapsed_time,
                print "\n\ntotal: %f\n" % total
