class Level( object ):
    """
    An enumeration of Draws with same amount drawn from the base by the given algorithm.
    """

    __slots__ = [ 'state' ]

    def __init__( self, algorithm, parent, iterable=[] ):
        from .grid import Grid
        from .draw import Draw
        from .pretty import Pretty

        if not issubclass(algorithm, Pretty):
            raise TypeError("algorithm is expected to be Pretty, it's %s instead" % type(algorithm))
        if not isinstance(parent, Grid):
            raise TypeError("parent of Level should be Grid type, it's %s instead" % type(parent))
        if not all(isinstance(d, Draw) for d in iterable):
            raise TypeError("a Level may only contain Draw")

        self.state = algorithm(parent, iterable)

    @property
    def P(self):
        return (d.P for d in self.state)

    def next_level( self, n=None, target=None ):

        """
        Enumerate the next Level.
        From each Draw draw one farther element and calculates the probabilities of them.
        The argument target limits the enumeration to only those events from which the target is reachable.
        The argument n can be given which equals to the number of the Levels already enumerated.
        """

        n = n or self.state.parent.roof - sum(self.state[0])
        target = target or [0] * self.state.parent.m

        following = self.state.next_level(n, target)

        if following:
            self.state = following
            return Level( following.__class__, following.parent, following)
        else:
            raise ValueError("Nothing follows an empty Level.")

    # proxies #

    def __str__( self, depth=1 ):
        return self.state.__str__(depth)

    def __repr__( self, depth=1 ):
        depth += 5
        return "Level(%s, %r,\n%s%s)" % ( self.state.__class__.__name__,
                                          self.state.parent,
                                          ' ' * depth,
                                          self.state.__repr__(depth + 1) )

    def __len__( self ):
        return len(self.state)

    def __getitem__( self, key ):
        if isinstance(key, slice):
            return self.state.__getitem__(key)
        return self.state.__getitem__(key)

    def __getslice__( self, i, j ):
        return self.state.__getslice__(i, j)

    def __setslice__( self, i, j, sequence ):
        return self.state.__setslice__(i, j, sequence)

    def __delslice__( self, i, j ):
        return self.state.__delslice__(i, j)
