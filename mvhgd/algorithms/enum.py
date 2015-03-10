from ..core import Pretty
from ..core import Draw
from ..utils import nCk


class Enumerate( Pretty ):
    def __init__( self, parent, iterable ):
        self.parent = parent
        super( Enumerate, self ).__init__( iterable )

    def next_level( self, n, target ):
        #n = self.parent.roof - denominator

        following = Enumerate( self.parent, [] )
        for d in self:
            for k in range( d.gamma, self.parent.m ):
                if d[k] > target[k]:
                    tmp_d = list( d )
                    tmp_d[k] -= 1
                    p = reduce( lambda x, y: x * y,
                                map(nCk, self.parent.root, tmp_d),
                                1.0 / nCk(self.parent.roof, n + 1) )
                    child = Draw( tmp_d, k, P=p )

                    following.append( child )

        return following