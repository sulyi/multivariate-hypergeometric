
class Pretty( list ):
     
    """
    overrides output string formats
    """
 
    def __init__( self, iterable=[] ):
        super( Pretty, self ).__init__( iterable )
         
    def __getslice__( self, i, j ):
        return Pretty( super( Pretty, self ).__getslice__( i, j ) )
 
    def __setslice__( self, i, j, sequence ):
        return Pretty( super( Pretty, self ).__setslice__( i, j, sequence ) )
  
    def __delslice__( self, i, j ):
        return Pretty( super( Pretty, self ).__delslice__( i, j ) )
 
    def __str__( self, depth=1 ):
        return '[ %s ]' % (',\n ' + ' ' * depth).join(
            i.__str__(depth + 2) if isinstance( i, Pretty ) else str(i) for i in self )
    
    def __repr__( self, depth=0 ):
        depth += len(self.__class__.__name__) + 2
        return '%s([ %s\n%s])' % ( self.__class__.__name__, (',\n ' + ' ' * depth).join(
            i.__repr__( depth + 1 ) if isinstance( i, Pretty ) else repr(i) for i in self ), ' ' * depth )
