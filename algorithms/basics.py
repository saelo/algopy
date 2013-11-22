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



def has_cycles(graph):
    """
    Returns a list of path objects, each making up a cycle in the provided graph.

    If there is no path and empty list will be returned.
    """
    if graph.empty():
        return []

    # initialization
    for node in graph.nodes():
        node.color = "white"

    # dfs from the first node
    res = _dfs_cycle(graph, graph.nodes()[0], Path(graph.nodes()[0]))

    # cleanup
    for node in graph.nodes():
        del node.color

    return res


def _dfs_cycle(graph, cur, path):
    cur.color = "grey"
    for edge in cur.outgoing_edges():
        n = edge.destination()
        if n.color == "white":
            path.append(edge, n)
            if _dfs_cycle(graph, n, path):
                return True
            # continue with next neighbor
            path.pop()
        elif n.color == "grey":
            # cycle detected
            return True

    # done with this node    
    cur.color = "black"
    return False
