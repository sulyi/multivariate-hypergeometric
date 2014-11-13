#/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
Created on 2014.10.15.

@author:  Ákos Sülyi
"""

import time
import core
from utils import nCk


def generate_input_data( seed, concatenation=1 ):
    
    if not hasattr( concatenation, '__iter__' ):
        concatenation = [ concatenation ]
        
    for i, c in enumerate( concatenation, 1 ):
        for d in range(1, c + 1):
            yield [ x * d for x in seed ] * i


def _combinatorial_generate( root, target=None ):
    roof = sum( root )
    m = len( root )
    
    floor = 1 if target is None else roof - sum( target )
    target = target or [ 0 ] * m
        
    previous = [ core.Draw( root ) ]
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
                    child = core.Draw( tmp_d, k, P=p )
                    
                    following.append( child )
        previous = following
        ##### end of next level mimic #####
        yield previous


def compare_test(data):
    g  =  core.Grid(data)
    cg = _combinatorial_generate(data)

    sct = 0.0
    st  = 0.0
    max_delta = 0.0

    for _i in range(g.roof):

        start = time.clock()
        level = g.next()
        st += time.clock() - start

        start = time.clock()
        c_level = cg.next()
        sct += time.clock() - start

        for j in range(len(level)):
            max_delta = max( max_delta, abs( level[j].P - c_level[j].P ) )

    return st, sct, max_delta


def cputime_test(data):
    n = 1
    full = 0.0
    while not full:
        for _i in range(n):
            start = time.clock()
            for _ in core.Grid(data):
                pass
            full += time.clock() - start
        full /= n
        n *= 10
    return full, n / 10


def c_cputime_test(data):
    n = 1
    full = 0.0
    while not full:
        for _i in range(n):
            start = time.clock()
            for _ in _combinatorial_generate(data):
                pass
            full += time.clock() - start
        full /= n
        n *= 10
    return full, n / 10