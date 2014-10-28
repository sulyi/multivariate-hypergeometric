from .case import Case 
from .level import Level

class Grid ( object ):
    
    '''
    '''
    # FIXME: doc Grid
    
    __slots__ = [ 'root', 'm', 'roof', 'lentab', '_iroot', '__weekref__' ]
    
    def __init__( self, supremum=[] ):
        self.root = Case(supremum)
        self.m = len(supremum)
        self.roof = sum(self.root)
        self.lentab = [ [1] for _i in range(self.m) ]
        self._iroot = [ sum(self.root[:i]) for i in range(self.m)  ]
    
    def __repr__( self ):
        return "Grid(%r)" % self.root
    
    def __str__( self ):
        return "Grid instance with supremum of %s" % self.root
    
    def generate( self, target=None ):
        floor = 0 if target is None else sum( target )
        target =  target or [ 0 ] * self.m
        
        previouse = Level( self, [ self.root ] )
        yield previouse
    
        for n in range( self.roof, floor, -1 ):
            previouse = previouse.next_level( n, target )
            yield previouse

    def combinatoric_length( self, n, i ):
        n_ast = n - self._iroot[i]
        return self.lentab[i][n_ast] if n_ast > 0 else 0 
