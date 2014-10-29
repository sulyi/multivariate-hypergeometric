from case import Case 
from level import Level


class Grid ( object ):

    """
    """
    # FIXME: doc Grid
    
    __slots__ = [ 'root', 'm', 'roof', 'len_tab', '_iroot', '__weekref__' ]

    def __init__( self, supremum=[] ):
        self.root = Case( supremum )
        self.m = len( supremum )
        self.roof = sum( self.root )
        self.len_tab = [ [1] for _i in range(self.m) ]
        self._iroot = [ sum(self.root[:i]) for i in range(self.m) ]

    def __repr__( self ):
        return "Grid(%r)" % self.root

    def __str__( self ):
        return "Grid instance with supremum of %s" % self.root

    def generate( self, target=None ):
        floor = 0 if target is None else sum( target )
        target =  target or [ 0 ] * self.m
        
        previous = Level( self, [ self.root ] )
        yield previous
    
        for n in range( self.roof, floor, -1 ):
            previous = previous.next_level( n, target )
            yield previous

    def read_len_tab( self, n, i ):
        n_ast = n - self._iroot[i]
        return self.len_tab[i][n_ast] if n_ast > 0 else 0
