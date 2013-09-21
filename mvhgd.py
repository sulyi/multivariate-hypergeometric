#/usr/bin/env python
#coding: UTF-8
'''
Combinatoric enumeration of the events of multivariate hypergeometric distribution   
and calculating their probabilities

Created on 2013.07.06.

@author: Ákos Sülyi
'''

import scipy 
import scipy.sparse
# FIXME: eclipse and it's warnings and/or errors, pfff

class Drawing(list):
    ''''
    event happened by drawing one element from an urn
    '''
    
    def __init__( self, iterable, gamma=0, delta=0):
        super( Drawing, self ).__init__( iterable )
        self.gamma = gamma
        self.delta = delta
        
    def __str__( self ):
        return '%s ~ (%d, %d)' % ( super( Drawing, self ).__repr__(),
                                   self.gamma,
                                   self.delta
                                 )
    
    def __repr__( self ):
        return 'Drawing( %s, %s, %s )' % ( super( Drawing, self ).__repr__(),
                                           self.gamma.__repr__(),
                                           self.delta.__repr__()
                                         )
    
    
    def draw_one_from_each_possible( self, reverse=False ):
        # FIXME: this is obsolete LEvel.next_level does this 
        '''
        enumerating possible drawings
        if a category has no element can't be drawn from it
        '''
        
        if reverse:
            self.reverse()
        for i in xrange(self.gamma, len(self)): # FIXME: Python 3 has only range
            if self[i]:
                child = Drawing( self, i )
                child[i] -= 1
                if reverse:
                    child.reverse()
                yield child
                
        if reverse:
            self.reverse()

                
def calculate( base ):
    ''' enumerating all possible drawing from base 
        and calculating transition weight matrices of levels
        of which product gives the probabilities of each element of the enumeration
        base contains number of elements in each category   
    '''
    summa = sum( base )
    previouse = Level( [ Drawing(base) ] )
    lattice = Pretty()
    
    for l in xrange( summa, 0, -1 ): # FIXME: Python 3 has only range
        lattice.append( previouse )
        previouse = previouse.next_level( True )
         
    return lattice
                
class Pretty( list ):
    '''overriding output string formats'''

    def __init__( self, iterable=[] ):
        super( Pretty, self ).__init__( iterable )
        
    def __str__( self, depth=1 ):
        return '[ %s ]' %  (',\n' + '  ' * depth).join( i.__str__(depth+1) if isinstance(i, Pretty) else str(i) for i in self )
   
    def __repr__( self, depth=1 ):
        return 'Pretty([ %s\n%s])' %  ( (',\n' + ' '*9*depth).join( i.__repr__(depth+1) if isinstance(i, Pretty) else repr (i) for i in self ), ' '*(9*depth-2) )

class Level( Pretty ):
    
    def __init__( self, iterable=[], tmatrix=scipy.array([]) ): # TODO: might needed to add dtypep and order
        if not all( isinstance( e, Drawing ) for e in iterable ):
            raise ValueError( 'a Level may only contain Drawing' )
        super( Level, self ).__init__( iterable )
        if iterable:
            if tmatrix.__nonzero__() is scipy.True_ :
                if tmatrix.shape[1] == len( iterable ):
                    self.tmatrix = tmatrix
                else:
                    raise ValueError( 'number of Drawing (%d) does not equal to number of columns of tmatrix (%d)' % ( tmatrix.shape[0], len(iterable) ))
            else:
                self.tmatrix = scipy.ones(( 1, len(iterable) )) # TODO: might needed to add dtypep and order
        else:
            self.tmatrix = scipy.empty(( 0, 0 ))
    
    # TODO: __str__ parse tmatrix, like previous version one that I've lost
    
    def next_level( self, reverse=False ):
        # TODO: turn this into a generator 
        
        if self:
            following = list()
            drawptr = list(0 for i in range(len(self[0])))
            basemidx = len(self[0]) - 1 # TODO: send this right to Hell

            data=list()
            indecies = list()
            indptr = list()
            
            indptr.append(len(indecies))
            
            for d in self:
                
                if reverse:
                    d.reverse()
                num_of_0s = d.gamma - d.delta
                    
                for i in xrange(len(d)): # FIXME: Python 3 has only range
                    
                    if i < d.gamma:
                        
                        if d[i]:
                            indecies.append(drawptr[i])
                            data.append(d[i])
                            test(d, following[drawptr[i]], basemidx - i) # TODO: also purge from this, or at least make it more decent
                            drawptr[i] += 1
                        elif drawptr[i] < len(following) and following[drawptr[i]].delta >= d.delta:
                                drawptr[i] = len(following)
                    else:
                        
                        if d[i]:
                            child = Drawing( d, i, i - num_of_0s)
                            child[i] -= 1
                            if reverse:
                                child.reverse()
                            indecies.append(len(following))
                            data.append(d[i])
                            following.append(child)
                        else:
                            num_of_0s += 1
                        drawptr[ i ] = len(following)
                            
                if reverse:
                    d.reverse()
                indptr.append(len(indecies))
                
            tmatrix = scipy.sparse.csr_matrix(( scipy.array(data), scipy.array(indecies), scipy.array(indptr) ))
            return Level( following, tmatrix )
        
        else:
            raise ValueError("Nothing follows an empty Level.")
        

# TODO: clean up, clean up, clean up

def test(oa,b,i):
    a = list(oa)
    midx= len(a)-1 
    for j in range(midx,-1,-1):
        a[j] -= b[midx-j]
    if sum(a) != 1 or a[midx-i] != 1:
        raise ValueError('%s %s %d' %(oa,b,i))

def str_iterable( l, depth=1 ):
    '''less object oriented approach to format output strings'''
    
    if type( l ) is list:
        _open = '['
        _close = '\n' + ' ' * (depth-1)  + ']'
    elif type( l ) is dict:
        _open = '{'
        _close = '\n' + ' ' * (depth-1) + '}'
    elif type( l ) is tuple:
        _open = '('
        _close = '\n' + ' ' * (depth-1) + ')'
    else:
        _open = ''.join(( l.__class__.__name__, '([' ))
        _close = '\n' + ' ' * (depth-1) + '])'
    depth += len( _open )
    return '%s %s %s' % ( _open,
                          (',\n' + ' ' * depth).join( str_iterable( i, depth+1 )
                                                         if hasattr( i, '__iter__' ) 
                                                         else str( i )
                                                            if not isinstance( i, str )
                                                            else '\'%s\'' %i
                                                      for i in l ),
                          _close )