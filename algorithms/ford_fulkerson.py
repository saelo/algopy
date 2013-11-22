#!/usr/bin/env python
#coding: UTF-8
#
# Implementation of the Ford-Fulkerson algorithm to solve the maximum flow problem.
#
# Copyright (c) 2013 Samuel Groß
#

from graph import *
from basics import depth_first_search


def solve_max_flow_ff(graph, s, t):
    """
    Solves the maximum flow prolem using the ford-fulkerson algorithm for the given 
    graph and source/target node.
    """

    while True:
        path = depth_first_search(graph, s, t)
        if path is None:
            break

        # find maximum capacity on the current path
        min_capacity = None
        for edge in path.edges():
            if min_capacity is None or edge.capacity < min_capacity:
                min_capacity = edge.capacity

        # subtract min_capacity from all edges and add return edge
        for edge in path.edges():
            edge.capacity -= min_capacity
            if not graph.has_reverse_edge(edge):
                graph.add_edge(edge.destination(), edge.source(), {"capacity" : min_capacity, "tmp" : True})
            else: 
                graph.get_reverse_edge(edge).capacity += min_capacity
            if edge.capacity == 0:
                graph.remove_edge(edge)

    # reverse edges and cleanup
    for edge in graph.edges():
        if hasattr(edge, "tmp"):
            if graph.has_reverse_edge(edge):
                graph.get_reverse_edge(edge).load = edge.capacity
            else:
                graph.add_edge(edge.destination(), edge.source(), {"load" : edge.capacity})
            graph.remove_edge(edge)
