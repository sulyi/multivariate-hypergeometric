import scipy.sparse
from ..core import Pretty
from ..core import Draw


class Descend( Pretty ):
    def __init__( self, parent, iterable, twmatrix=None ):
        self.parent = parent
        if twmatrix is None:
            twmatrix = scipy.sparse.csc_matrix( scipy.ones(( 1, len(iterable) )) )
        self.twmatrix = twmatrix
        super( Descend, self ).__init__( iterable )

    def next_level( self, n, target ):
        following = list()
        gammas = list()
        drawptr = list( 0 for _ in range(self.parent.m) )
        data = list()
        indices = list()
        indptr = [ 0 ]

        for d in self:
            delta = sum( x > 0 for x in d[:d.gamma] )
            num_of_0s = d.gamma - delta

            for i, k in enumerate(d):
                if i >= d.gamma:
                    if k > target[i]:
                        child = list( d )
                        child[i] -= 1
                        indices.append( len(following) )
                        data.append( k )
                        following.append( child )
                        gammas.append( i )
                    else:
                        num_of_0s += 1
                    drawptr[i] = len(following)
                else:
                    if k > target[i]:
                        indices.append( drawptr[i] )
                        data.append(k)
                        drawptr[i] += 1
                    elif ( drawptr[i] < len(following) and
                           sum( x > 0 for x in following[drawptr[i]][:gammas[drawptr[i]]] ) >= delta ):
                        drawptr[ i ] = len(following)

            indptr.append( len(indices) )
        twm = scipy.sparse.csc_matrix(( scipy.array(data), scipy.array(indices), scipy.array(indptr) ))
        p = (twm / (self.parent.roof - n)) * scipy.array( [d.P for d in self] )

        return Descend( self.parent, map(Draw, following, gammas, p), twm )