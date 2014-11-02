from .case import Case
from .level import Level
from ..utils import nCik


class Grid ( object ):

    """
    """
    # FIXME: doc, Grid
    
    __slots__ = [ 'root', 'm', 'roof', 'len_tab', '_iroot', '_psos' ]

    def __init__( self, supremum=[] ):
        self.root = Case( supremum )
        self.m = len( supremum )
        self.roof = sum( self.root )
        self.len_tab = [ [1] for _i in range(self.m) ]
        self._iroot = [ sum(self.root[:i]) for i in range(self.m) ]
        self._psos = self._power_set_ordered_by_sums()

    def __repr__( self ):
        return "Grid(%r)" % self.root

    def __str__( self ):
        return "Grid instance with supremum of %s" % self.root

    def generate( self, target=None ):
        floor = 0 if target is None else sum( target )
        target = target or [ 0 ] * self.m
        
        previous = Level( self, [ self.root ] )
        yield previous
    
        for n in range( self.roof, floor, -1 ):
            previous = previous.next_level( n, target )
            yield previous

    def read_len_tab( self, n, i ):
        n_ast = n - self._iroot[i]
        return self.len_tab[i][n_ast] if n_ast >= 0 else 0

    def _power_set_ordered_by_sums( self ):

        """
        """
        # TODO: doc, _power_set_ordered_by_sums, http://math.stackexchange.com/questions/89419/

        # FIXME: lose ordering input
        n = list( self.root )
        n.sort()

        s = [(0, 0)]
        l = [[]]
        a = [ 0 ] * self.m

        while any( a is not None for a in a):
            min_s = None
            for i, a_ast in enumerate(a):
                if a_ast is not None:
                    curr_s = n[i] + s[a_ast][1]
                else:
                    continue
                if min_s > curr_s or min_s is None:
                    min_s = curr_s
                    i_ast = i
                elif min_s == curr_s and s[a_ast][0] < s[a[i_ast]][0]:
                    i_ast = i
            l_new = list( l[a[i_ast]] )
            l_new.append(( i_ast, n[i_ast] ))
            l.append( l_new )
            s.append(( len(l_new), min_s ))

            a[i_ast] += 1

            # FIXME: lover indexed elements must be lover in value, leading to need of ordering input
            while not all(n[i_ast] >= item and j < i_ast for j, item in l[a[i_ast]]):
                a[i_ast] += 1
                if a[i_ast] == len(s):
                    a[i_ast] = None
                    break
        return s

    def calculate_length( self, n ):

        """
        """
        #TODO: doc, calculate length

        members = 0
        while n + 1 > sum( self._psos[members] ):
            members += 1
        return sum( (-1) ** self._psos[i][0] * nCik( self.m, n - sum(self._psos[i]) ) for i in range(members) )