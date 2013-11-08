#!/usr/bin/env python
#coding: UTF-8
#
# Basic graph algorithms.
#
# Copyright (c) 2013 Samuel Groß
#

from graph import *

def depth_first_search(graph, s, t):
    """
    Find a path from the source to the target by using depth first search.

    Returns a path object connecting s and t or None if there is no such path.
    """
    # initialization
    for node in graph.nodes():
        node.visited = False

    # dfs from the start node
    path = Path(s)
    if not _dfs(graph, s, t, path):
        path = None

    # cleanup
    for node in graph.nodes():
        del node.visited

    return path


def _dfs(graph, cur, t, path):
    cur.visited = True
    for edge in cur.outgoing_edges():
        n = edge.destination()
        if not n.visited:
            path.append(edge, n)
            if n == t or _dfs(graph, n, t, path): 
                return True
            # continue with next neighbor
            path.pop()
                
    # done with this node    
    return False
