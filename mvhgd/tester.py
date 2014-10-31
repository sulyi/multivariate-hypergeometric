#/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
Created on 2014.10.15.

@author:  Ákos Sülyi
"""

import time
import core
from utils import nCk


def generate_input_data( seed, concat=1 ):
    
    if not hasattr( concat, '__iter__' ):
        concat = [ concat ]
        
    for i, c in enumerate( concat, 1 ):
        for d in range(1, c + 1):
            yield map(lambda x: x * d, seed) * i


def _combinatorial_generate( root, target=None ):
    roof = sum( root )
    m = len( root )
    
    floor = 1 if target is None else roof - sum( target )
    target = target or [ 0 ] * m
        
    previous = [ core.Case( root ) ]
    yield previous
    
    for n in range( floor, roof + 1 ):
        ######## next level mimic ########
        following = []
        for d in previous:
            for k in range( d.gamma, m ):
                if d[k] > target[k]:
                    tmp_d = list( d )
                    tmp_d[k] -= 1
                    p = reduce(lambda x, y: x * y, map( nCk, root, tmp_d ), 1.0 / nCk( roof, n) )
                    child = core.Case( tmp_d, k, P=p )
                    
                    following.append( child )
        previous = following
        ##### end of next level mimic #####
        yield previous


def compare_test(data):
    G  = core.Grid(data)
    g  = G.generate()
    cg = _combinatorial_generate(data)
    
    sct = 0.0
    st  = 0.0
    max_delta = 0.0
    
    for _i in range(G.roof):

        start = time.clock()
        L = g.next()
        st += time.clock() - start
         
        start = time.clock()
        cL = cg.next()
        sct += time.clock() - start
        
        for j in range(len(L)):
            max_delta = max( max_delta, abs( L[j].P - cL[j].P ) )
                
    return st, sct, max_delta


def cputime_test(data):
    start = time.clock()
    for _l in core.Grid(data).generate():
        pass
    return time.clock() - start
