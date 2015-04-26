from ..core import Pretty
from ..core import Draw


class Zigzag( Pretty ):
    def __init__( self, parent, iterable ):
        self.parent = parent
        super( Zigzag, self ).__init__( iterable )

    def next_level( self, n, target ):
        denominator = self.parent.roof - n

        flush = [ None ] * self.parent.m
        drawptr = [ self.parent._read_len_tab( n, i ) for i in range( 1, self.parent.m ) ]
        drawptr.append( 0 )

        following = Zigzag( self.parent, [] )

        for i, d in enumerate( self ):
            num_of_0s = d.gamma - sum( x > target[j] for j, x in enumerate(d[:d.gamma]) )
            for k in range( d.gamma, self.parent.m ):
                flush[ k - num_of_0s ] = len( following )

                # enumerating descendants
                if d[k] > target[k]:
                    p = d.P * d[k]
                    drawptr[k] += 1

                    # finding other ascendants
                    for j, c in enumerate( d ):
                        if j != k and c < self.parent.root[j]:
                            # skipping
                            if drawptr[j] <= i:
                                drawptr[j] = i + ( self.parent._read_len_tab( n - sum(target) + sum(d[:j]), j + 1 ) or 1 )
                            # stepping
                            p += self[drawptr[j]].P * (c + 1)
                            drawptr[j] += 1

                    child = Draw( d, k, p / denominator )
                    child[k] -= 1
                    following.append( child )

                else:
                    num_of_0s += 1

        # storing length of shifted level of each fixed prefix sublattice
        for i, f in enumerate( flush ):
            if f is not None:
                self.parent._len_tab[i].append( len( following ) - f )

        return following