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

        """
        """
        # TODO: doc, limit_to

        if target is not None:
            try:
                if len(target) == 1:
                    raise TypeError
                elif len(target) != self.m:
                    raise ValueError( "argument has different number of categories (%d) than Grid (%d)" %
                                      (len(target), self.m) )
                target = Draw(target)
                if not Draw([0] * self.m) <= target <= self.root:
                    raise ValueError( "argument should be between %s and %s" % ([0] * self.m, list(self.root)) )
                floor = sum(target)
            except TypeError:
                floor = self.roof - int(target)
                if not 0 < floor < self.roof:
                    raise ValueError( "argument should be between Grid.roof (%d) and 0" % self.roof )
                target = [0] * self.m
        else:
            floor = 0
            target = [0] * self.m
        previous = Level( self, [ self.root ] )
        yield previous

        for n in range( self.roof, floor, -1 ):
            previous = previous.next_level( n, target )
            yield previous

    def _read_len_tab( self, n, i ):
        # unsafe, since _len_tab is filled during generation
        n_ast = n - self._iroot[i]
        return self._len_tab[i][n_ast] if n_ast >= 0 else 0