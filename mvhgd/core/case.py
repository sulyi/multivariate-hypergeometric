class Case(bytearray):
    """
    an event happened by drawing elements from an urn containing elements falling under different categories,
    the number of drawn elements in each category is given by an iterable
    """

    __slots__ = ['gamma', 'delta', 'P']

    def __init__(self, iterable=None, gamma=0, delta=0, P=1.0):
        if iterable is not None:
            try:
                super(Case, self).__init__(map(int, iterable))
            except TypeError:
                raise ( TypeError, "itreable must support iteration" )
            except ValueError:
                raise ( ValueError, "each item in iterable must be an integer in range(0, 256)" )
        else:
            super(Case, self).__init__()
        self.gamma = gamma
        self.delta = delta
        # fractional data type for P would be be swell as far as numeric stability goes,
        # but again that would make values grow factorially in size
        self.P = P

    def __eq__(self, other):
        if not isinstance(other, Case):
            return False
        return super(Case, self).__eq__(other) and self.gamma == other.gamma and self.delta == other.delta

    def __str__(self):
        return '%s ~ (%d, %s) - %r' % ( list(self),
                                        self.gamma,
                                        self.delta,
                                        self.P
                                        )

    def __repr__(self):
        return 'Case( %s, %r, %r, %r )' % ( list(self),
                                            self.gamma,
                                            self.delta,
                                            self.P
                                            )