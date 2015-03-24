class Draw(list):
    """
    An event happened by drawing elements from an urn containing elements falling under different categories.
    The number of elements still remaining in each category is given by an iterable.
    """

    __slots__ = [ 'gamma', 'P' ]

    def __init__( self, iterable=None, gamma=0, P=1.0 ):
        if iterable is not None:
            try:
                super(Draw, self).__init__(int(i) for i in iterable)
            except TypeError:
                raise TypeError("argument must support iteration")
        else:
            super(Draw, self).__init__()
        self.gamma = gamma
        # fractional data type for P would be be swell as far as numeric stability goes,
        # but again that would make values grow factorially in size
        self.P = P

    def __gt__( self, other ):
        if len(self) != len(other):
            return False
        return all(o < d for o, d in zip(other, self))

    def __lt__( self, other ):
        if len(self) != len(other):
            return False
        return all(o > d for o, d in zip(other, self))

    def __ge__( self, other ):
        if len(self) != len(other):
            return False
        return all(o <= d for o, d in zip(other, self))

    def __le__( self, other ):
        if len(self) != len(other):
            return False
        return all(o >= d for o, d in zip(other, self))

    def __eq__( self, other ):
        if not isinstance(other, Draw):
            return False
        return super(Draw, self).__eq__(other) and self.gamma == other.gamma

    def __str__( self ):
        return '%s ~ (%d) - %r' % ( list(self),
                                    self.gamma,
                                    self.P
                                    )

    def __repr__( self ):
        return 'Draw(%s, %r, %r)' % ( list(self),
                                      self.gamma,
                                      self.P
                                      )