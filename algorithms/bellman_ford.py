#!/usr/bin/env python
#coding: UTF-8
#
# Implementation of the Bellman-Ford algorithm to calculate shortests pathes and detect negative cost cylces.
#
# Copyright (c) 2013 Samuel Groß
#

from graph import *
import sys


def bellman_ford_cycle(graph):
    """
    Runs the bellman ford algorithm to detect a negative cost cycle.

    The result is either a negative cost cycle or None if no such cycle exists in the given graph.
    """
    res = None

    # initialization
    for node in graph.nodes():
        node.dist = sys.maxsize
        node.predecessor = None

    # actual Bellman-Ford algorithm
    for i in range(len(graph.nodes())):
        for edge in graph.edges():
            if edge.source().dist + edge.cost < edge.destination().dist:
                edge.destination().dist = edge.source().dist + edge.cost
                edge.destination().predecessor = edge.source()

    # check for a negative cost cycles and reconstruct it
    for edge in graph.edges():
        if edge.source().dist + edge.cost < edge.destination().dist:
            path = []
            cur = edge.source()
            while not cur in path:
                path.append(cur)
                cur = cur.predecessor
            path.reverse()

            cycle = Path(cur)
            for node in path[:path.index(cur) + 1]:
                cycle.append(node.edge_from(cur), node)
                cur = node
            
            res = cycle
            break

    # cleanup
    for node in graph.nodes():
        del node.dist
        del node.predecessor

    return res
