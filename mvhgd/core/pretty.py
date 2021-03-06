from .level import Level


class Pretty( list ):
     
    """
    Override output string formats to be able to keep indentation.
    """
 
    def __init__( self, iterable=[] ):
        super( Pretty, self ).__init__( iterable )

    def __str__( self, depth=1 ):
        return '[ %s ]' % (',\n ' + ' ' * depth).join(
            i.__str__(depth + 2) if isinstance( i, (Pretty, Level) ) else str(i) for i in self )
    
    def __repr__( self, depth=1 ):
        depth += len(self.__class__.__name__) + 1
        return '%s([%s\n%s])' % ( self.__class__.__name__, (',\n' + ' ' * depth).join(
            i.__repr__(depth + 1) if isinstance( i, (Pretty, Level) ) else repr(i) for i in self ), ' ' * (depth - 1) )

    # just keeping Pretty

    def __getitem__( self, key ):
        if isinstance(key, slice):
            return Pretty( super( Pretty, self ).__getitem__( key ) )
        return super( Pretty, self ).__getitem__( key )

    def __getslice__( self, i, j ):
        return Pretty( super( Pretty, self ).__getslice__( i, j ) )

    def __setslice__( self, i, j, sequence ):
        return Pretty( super( Pretty, self ).__setslice__( i, j, sequence ) )

    def __delslice__( self, i, j ):
        return Pretty( super( Pretty, self ).__delslice__( i, j ) )
