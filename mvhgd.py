#/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Combinatoric enumeration of the events of multivariate hypergeometric distribution   
and calculating their probabilities

see also: doc at calculate method

Created on 2013.07.06.

@author: Ákos Sülyi
'''

import scipy.sparse

class Drawing(list):
    ''''
    an event happened by drawing elements from an urn containing elements falling under different categories,
    the number of drawn elements in each category is given by an iterable  
    gamma and delta variables are aiding the enumeration of these events
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
                
class Pretty( list ):
    '''overriding output string formats'''

    def __init__( self, iterable=[] ):
        super( Pretty, self ).__init__( iterable )
        
    def __str__( self, depth=1 ):
        return '\n[ %s ]' %  (',\n '+' ' * depth).join( i.__str__(depth+2) if isinstance(i, Pretty) else str(i) for i in self )
   
    def __repr__( self, depth=0 ):
        depth+=len(self.__class__.__name__)+3
        return '\n%s([ %s\n%s])' %  ( self.__class__.__name__, (',\n'+' '*depth).join( i.__repr__(depth) if isinstance(i, Pretty) else repr (i) for i in self ), ' '*(depth-1) )

class Level( Pretty ):
    '''a enumeration of Drawing with same amount drawn from the base, hence sum of elements in the categories are equal
       root Level should be initialized with an iterable containing a single base Drawing and [ 1 ] as twmatrix or without any twmatrix
       other Levels should be generated by next_level method
       the values of twmatrix are conditional probability and equal the probability of a Drawing from the current Level to occur if an event from the previouse Level is known to occur
       each column belong to the element with corresponding index in the current level
       each row belongs to the element with the corresponding index in the previouse Level
       tw stands for transition weight 
    '''
    
    def __init__( self, iterable=[], twmatrix=None ):
        # fractional data type would be be swell as far as numeric stability goes,
        # but again that would make numerator and denominator in products of matrices grow factorially
          
        if not all( isinstance( e, Drawing ) for e in iterable ):
            raise ValueError( 'a Level may only contain Drawing' )
        
        super( Level, self ).__init__( iterable )
        
        if iterable:
            if twmatrix is not None:
                if twmatrix.shape[0] == len( iterable ):
                    self.twmatrix = twmatrix
                else:
                    raise ValueError( 'number of Drawing (%d) does not equal to number of columns of twmatrix (%d)' % ( twmatrix.shape[0], len(iterable) ))
            else:
                # I don't think this has any sense unless len(iterable) = 1 
                self.twmatrix = scipy.sparse.csc_matrix( scipy.ones(( 1, len(iterable) )) )
        else:
            self.twmatrix = scipy.empty(( 0, 0 ))
            
    
    # TODO: __str__ parser for twmatrix, that can show which branch of the algorithm added the value / Drawing
     
    def next_level( self, target=None, denominator=None ):
        '''enumerates the next Level, draws one farther element from each Drawing
           target limits the enumeration to only those events from which the target is reachable
           also calculates next Level's twmatrix
        '''
        
        if self:
            if denominator:
                denominator = float(denominator)
            else:
                denominator = float(sum(self[0]))
                
            following = Pretty() # list() when it's not debuged   
            drawptr = list( 0 for i in range(len(self[0])) )

            data=list()
            indices = list()
            indptr = list()
            
            if target is None:
                # cloning zeros
                target = list(drawptr)
            
            indptr.append(len(indices))
            
            for d in self:
                
                num_of_0s = d.gamma - d.delta
                    
                for i,k in enumerate(d): 
                    
                    if i > d.gamma:
                        
                        if k  > target[i]:
                            child = Drawing( d, i, i-num_of_0s )
                            child[i] -= 1
                            indices.append( len(following) )
                            data.append( k )
                            following.append( child )
                        else:
                            num_of_0s += 1
                        drawptr [i] = len(following)
                    
                    else:
                        
                        debug =  len(following), drawptr[i] < len(following), drawptr[i] < len(following) and following[drawptr[i]].delta >= d.delta
                        if k > target[i]:
                            indices.append( drawptr[i] )
                            data.append(k)
                            drawptr[i] += 1
                        elif drawptr[i] < len(following) and following[drawptr[i]].delta >= d.delta:
                                drawptr[ i ] = len(following)                    
                            
                indptr.append( len(indices) )
            
            twm = scipy.sparse.csc_matrix(( scipy.array(data), scipy.array(indices), scipy.array(indptr) )) / denominator
            return Level( following, twm )
        
        else:
            raise ValueError( "Nothing follows an empty Level." )


def calculate( base, target=None ):
    ''' enumerating all possible Drawing from base
        base contains number of elements in each category
        target limits the enumeration to only those from which the target is reachable    
        and calculating transition weight matrices of Levels
        product of twmatrices of previous Levels gives the probabilities of each Drawing of a Level
        
        see also: doc at Level
    '''
    
    roof = sum( base )
    floor = 0 if target is None else sum( target )
    
    previouse = Level( [ Drawing( base ) ] )
    
    lattice = Pretty()
    lattice.append( previouse )
        
    for l in range( roof, floor, -1 ):
        previouse = previouse.next_level( target, l )
        lattice.append( previouse )
         
    return lattice
