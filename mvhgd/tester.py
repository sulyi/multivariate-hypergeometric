#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
Created on 2014.10.15.

@author:  Ákos Sülyi
"""

import time
from core import Grid


def generate_input_data( seed, concatenation=1 ):
    
    if not hasattr( concatenation, '__iter__' ):
        concatenation = [ concatenation ]
        
    for i, c in enumerate( concatenation, 1 ):
        for d in range(1, c + 1):
            yield [ x * d for x in seed ] * i


def compare_test(algorithm1, algorithm2, data):
    g1 = Grid(algorithm1, data)
    g2 = Grid(algorithm2, data)

    st1 = 0.0
    st2 = 0.0
    max_delta = 0.0

    for _i in range(g.roof):

        start = time.clock()
        level1 = g1.next()
        st1 += time.clock() - start

        start = time.clock()
        level2 = g2.next()
        st2 += time.clock() - start

        for j in range(len(level1)):
            max_delta = max( max_delta, abs( level1[j].P - level2[j].P ) )

    return st1, st2, max_delta


def cputime_test(algorithm, data):
    n = 1
    full = 0.0
    while not full:
        for _i in range(n):
            start = time.clock()
            for _ in Grid(algorithm, data):
                pass
            full += time.clock() - start
        full /= n
        n *= 10
    return full, n / 10