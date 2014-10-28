#/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Created on 2014.10.15.

@author:  Ákos Sülyi
'''

import time
import core
from utils import nCk

def generate_input_data( seed, concat=1 ):
    
    if not hasattr( concat, "__iter__" ):
        concat =  [ concat ]
        
    for i,c in enumerate( concat, 1 ):
        for d in range(1,c+1):
            yield map(lambda x: x * d,  seed)  * i

def _combinatoric_generate( root, target=None ):
    roof = sum( root )
    m = len( root )
    
    floor = 1 if target is None else roof - sum( target )
    target = target or [ 0 ] * m
        
    previouse = [ core.Case( root ) ]
    yield previouse
    
    for n in range( floor, roof + 1 ):
        following = []
        ######## next level mimic ########
        for d in previouse:
            for k in range( d.gamma, m ):
                if d[k]  > target[k]:
                    tmp_d = list( d )
                    tmp_d[k] -= 1
                    P = reduce(lambda x,y: x*y, map( nCk, root, tmp_d ), 1.0 / nCk( roof, n) )
                    child = core.Case( tmp_d, k, P=P ) 
                    
                    following.append( child )
                    
        yield following
        ##### end of next level mimic #####
        previouse = following

def compare_test(data):
    G   = core.Grid(data)
    g   = G.generate()
    cg  = _combinatoric_generate(data)
    
    sct = 0.0
    st  = 0.0
    maxDelta = 0.0
    
    for _i in range(G.roof):

        start = time.clock()
        L  = g.next()
        st += time.clock() - start
         
        start = time.clock()
        cL = cg.next()
        sct += time.clock() - start
        
        for j in range(len(L)):
            maxDelta = max( maxDelta, abs( L[j].P - cL[j].P ) )
                
    return st,sct,maxDelta

def cputime_test(data):
    start = time.clock()
    for _l in core.Grid(data).generate():
        pass
    return time.clock() - start
