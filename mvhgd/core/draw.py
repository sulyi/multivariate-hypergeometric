
class Draw ( bytearray ):

    """
    an event happened by drawing elements from an urn containing elements falling under different categories,
    the number of drawn elements in each category is given by an iterable
    """

    __slots__ = ['gamma', 'P']

    def __init__(self, iterable=None, gamma=0, P=1.0):
        if iterable is not None:
            try:
                super(Draw, self).__init__(map(int, iterable))
            except TypeError:
                raise ( TypeError, "iterable must support iteration" )
            except ValueError:
                raise ( ValueError, "each item in iterable must be an integer in range(0, 256)" )
        else:
            super(Draw, self).__init__()
        self.gamma = gamma
        # fractional data type for P would be be swell as far as numeric stability goes,
        # but again that would make values grow factorially in size
        self.P = P

    def __eq__(self, other):
        if not isinstance(other, Draw):
            return False
        return super(Draw, self).__eq__(other) and self.gamma == other.gamma

    def __str__(self):
        return '%s ~ (%d) - %r' % ( list(self),
                                    self.gamma,
                                    self.P
                                    )

    def __repr__(self):
        return 'Drawing( %s, %r, %r )' % ( list(self),
                                        self.gamma,
                                        self.P
                                        )