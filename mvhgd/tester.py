#/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Created on 2014.10.15.

@author:  Ákos Sülyi
'''

import time
import core

def generate_input_data( seed, concat=1 ):
    
    if not hasattr( concat, "__iter__" ):
        concat =  [ concat ]
        
    for i,c in enumerate( concat, 1 ):
        for d in range(1,c+1):
            yield map(lambda x: x * d,  seed)  * i

def compare_test(data):
    G   = core.Grid(data)
    g   = G.generate()
    cg  = G.combinatoric_generate()
    
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
                
    return sct,st,maxDelta

def cputime_test(data):
    start = time.clock()
    for _l in core.Grid(data).generate():
        pass
    return time.clock() - start
