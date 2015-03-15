from .draw import Draw
from .level import Level


class Grid ( object ):
    """

    """

    __slots__ = [ 'algorithm', 'root', 'roof', 'm', '_generator', '_len_tab', '_iroot' ]

    def __init__( self, algorithm, supremum=[] ):
        self.algorithm = algorithm
        self.root = Draw( supremum )
        self.m = len( supremum )
        self.roof = sum( self.root )
        self._len_tab = [ [1] for _ in range(self.m) ]
        self._iroot = [ sum(self.root[:i]) for i in range(self.m) ]
        self._generator = self._limit_traversal_to( None )

    def __repr__( self ):
        return "Grid(%s, %r)" % (self.algorithm.__name__, self.root)

    def __str__( self ):
        return "Grid instance with %s algorithm and supremum of %s" % (self.root, self.algorithm)

    def __iter__(self):
        return self._generator

    # Python 3 compatibility
    def __next__(self):
        return next( self._generator )

    # Python 2 compatibility
    def next(self):
        return next( self._generator )

    def limit_traversal_to( self, target=None ):
        """
        """
        # TODO: doc, limit_to
        self._generator = self._limit_traversal_to( target )

    def _limit_traversal_to( self, target ):
        if target is not None:
            if not hasattr(target, '__len__'):
                floor = self.roof - int(target)
                target = Draw([0] * self.m)
                if not 0 <= floor <= self.roof:
                    raise ValueError( "argument should be between Grid.roof (%d) and 0" % self.roof )
            elif len(target) == self.m:
                floor = sum(target)
                target = Draw(target)
                if not Draw([0] * self.m) <= target <= self.root:
                    raise ValueError( "argument should be between %s and %s" % ([0] * self.m, list(self.root)) )
            else:
                raise ValueError( "argument has different number of categories (%d) than Grid (%d)" %
                                  (len(target), self.m) )
        else:
            floor = 0
            target = Draw([0] * self.m)

        previous = Level( self.algorithm, self, [ self.root ] )
        yield previous
        for n in range( floor, self.roof ):
            previous = previous.next_level( n, target )
            yield previous

    def _read_len_tab( self, n, i ):
        # unsafe, since _len_tab is filled during generation
        n_ast = n - self._iroot[i]
        return self._len_tab[i][n_ast] if n_ast >= 0 else 0