from .draw import Draw
from .level import Level


class Grid ( object ):
    """
    A generator enumerating Levels of Draws, see also there.
    """

    __slots__ = [ 'algorithm', 'root', 'roof', 'm', '_generator', '_len_tab', '_iroot' ]

    def __init__( self, algorithm, supremum=[] ):
        self.algorithm = algorithm
        self.root = Draw( supremum )
        self.m = len( supremum )
        self.roof = sum( self.root )
        self._len_tab = [ [1] for _ in range(self.m) ]
        self._iroot = [ sum(self.root[:i]) for i in range(self.m) ]
        self._generator = self.generator()

    def __repr__( self ):
        return "Grid(%s, %r)" % (self.algorithm.__name__, self.root)

    def __str__( self ):
        return "Grid instance with %s algorithm and supremum of %s" % (self.root, self.algorithm)

    def __iter__(self):
        return self._generator

    def next(self):
        return next( self._generator )

    def limit_traversal_to( self, target=None ):
        """
        Set the internal _generator of the Grid.
        see also: generator
        """
        self._generator = self.generator( target )
        return self

    def generator( self, target=None ):
        """
        Create a generator to enumerate Levels from root of the Grid.
        Argument target limits traversal, can be int() or iterable, see also Level.next_level.
        """

        if target is not None:
            if not hasattr(target, '__len__'):
                roof = int(target)
                target = Draw([0] * self.m)
                if not 0 <= roof <= self.roof:
                    raise ValueError( "argument should be between Grid.roof (%d) and 0" % self.roof )
            elif len(target) == self.m:
                roof = sum(target)
                target = Draw(target)
                if not Draw([0] * self.m) <= target <= self.root:
                    raise ValueError( "argument should be between %s and %s" % ([0] * self.m, list(self.root)) )
            else:
                raise ValueError( "argument has different number of categories (%d) than Grid (%d)" %
                                  (len(target), self.m) )
        else:
            roof = self.roof
            target = Draw([0] * self.m)

        previous = Level( self.algorithm, self, [ self.root ] )
        yield previous
        for n in range( roof ):
            previous = previous.next_level( n, target )
            yield previous

    def _read_len_tab( self, n, i ):
        # unsafe, since _len_tab is filled during generation
        n_ast = n - self._iroot[i]
        return self._len_tab[i][n_ast] if n_ast >= 0 else 0