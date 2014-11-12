from draw import Draw
from level import Level


class Grid ( object ):

    """
    """
    # TODO: doc, Grid
    
    __slots__ = [ 'root', 'm', 'roof', '_default', '_len_tab', '_iroot' ]

    def __init__( self, supremum=[] ):
        self.root = Draw( supremum )
        self.m = len( supremum )
        self.roof = sum( self.root )
        self._len_tab = [ [1] for _ in range(self.m) ]
        self._iroot = [ sum(self.root[:i]) for i in range(self.m) ]
        self._default = self.limit_to()

    def __repr__( self ):
        return "Grid(%r)" % self.root

    def __str__( self ):
        return "Grid instance with supremum of %s" % self.root

    def __iter__(self):
        return self._default

    # Python 3 compatibility
    def __next__(self):
        return next( self._default )

    # Python 2 compatibility
    def next(self):
        return next( self._default )

    def limit_to( self, target=None ):
        # TODO: support limitation by depth
        # TODO: target validation
        floor = 0 if target is None else sum( target )
        target = target or [ 0 ] * self.m

        previous = Level( self, [ self.root ] )
        yield previous
    
        for n in range( self.roof, floor, -1 ):
            previous = previous.next_level( n, target )
            yield previous

    def _read_len_tab( self, n, i ):
        n_ast = n - self._iroot[i]
        return self._len_tab[i][n_ast] if n_ast >= 0 else 0