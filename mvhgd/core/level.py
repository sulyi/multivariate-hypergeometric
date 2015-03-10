from draw import Draw
from pretty import Pretty


class Level( object ):
    """
    a enumeration of Draws with same amount drawn from the base, hence sum of elements in the categories are equal
    root Level should be initialized with an iterable containing a single base Draw
    other Levels should be generated by next_level method
    """

    __slots__ = [ 'state' ]

    def __init__(self, algorithm, parent, iterable=[]):
        from grid import Grid

        if not issubclass(algorithm, Pretty):
            raise TypeError("algorithm is expected to be Pretty")
        if not isinstance(parent, Grid):
            raise TypeError("parent of Level should be Grid type it's %s instead" % type(parent))
        if not all(isinstance(d, Draw) for d in iterable):
            raise TypeError("a Level may only contain Draw")

        self.state = algorithm(parent, iterable)

    @property
    def P(self):
        return (d.P for d in self.state)

    def next_level(self, n=None, target=None):

        """
        enumerates the next Level,
        draws one farther element from each Draw and calculates the probabilities of them
        target limits the enumeration to only those events from which the target is reachable
        denominator can be given which equals to the number of the Levels already enumerated
        """

        n = n or self.state.parent.roof - sum(self.state[0])
        target = target or [0] * self.state.parent.m

        following = self.state.next_level(n, target)

        if following:
            self.state = following
            return self
        else:
            raise ValueError("Nothing follows an empty Level.")

    # proxies #

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        algorithm_param = self.state.__class__.__name__
        parent_param = repr(self.state.parent)
        return "Level(%s, %s, %s)" % ( algorithm_param,
                                       parent_param,
                                       self.state.__repr__(len(algorithm_param) + len(parent_param) + 10) )

    def __len__(self):
        return len(self.state)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.state.__getitem__(key)
        return self.state.__getitem__(key)

    def __getslice__(self, i, j):
        return self.state.__getslice__(i, j)

    def __setslice__(self, i, j, sequence):
        return self.state.__setslice__(i, j, sequence)

    def __delslice__(self, i, j):
        return self.state.__delslice__(i, j)
