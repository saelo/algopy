#!/usr/bin/env python
#coding: UTF-8
#
# Implementation of the push-relabel algorithm to solve the max flow problem.
#
# Copyright (c) 2013 Samuel Groß
#

from graph import *


def _get_active_node(graph, s, t):
    for node in graph.nodes():
        if not node == t and not node == s and node.overrun > 0:
            return node

    return None

def _has_active_node(graph, s, t):
    return True if not _get_active_node(graph, s, t) == None else False

def _push(node):
    """
    Push load away from the current node if possible.

    If a neighboring node which is "closer" to the target can accept more load
    push it to the node. If no such node is found push fails meaning a relabel has
    to be executed.
    """
    success = False
    for edge in node.outgoing_edges():
        neighbor = edge.destination()
        if not node.dist == neighbor.dist + 1 or edge.load == edge.capacity:
            continue
        success = True
        reverse_edge = node.edge_from(neighbor)

        push = min(edge.capacity - edge.load, node.overrun)
        edge.load         += push
        reverse_edge.load -= push
        neighbor.overrun  += push
        node.overrun      -= push

        print("pushing %i from %s to %s" % (push, node.name(), neighbor.name()))

        if node.overrun == 0:
            break

    return success

def _relabel(node):
    """
    Relabel a node.

    Adjusts the dist value of the current node to the minimun dist
    value of its neighbors plus one.
    """
    min_dist = None
    for edge in node.outgoing_edges():
        if edge.load == edge.capacity:
            continue
        if min_dist == None or edge.destination().dist < min_dist:
            min_dist = edge.destination().dist

    node.dist = min_dist + 1
        

def solve_max_flow(graph, s, t):
    """
    Solves the max flow prolem using the push-relabel algorithm for the given 
    graph and source/target node.
    """
    #
    # initialize algorithm specific data
    #
    for node in graph.nodes():
        node.dist = 0
        node.overrun = 0
    for edge in graph.edges():
        edge.load = 0
        # add return edges
        if not graph.has_reverse_edge(edge):
            graph.add_edge(edge.destination(), edge.source(), {"capacity" : 0, "load" : 0, "tmp" : True})
    # initialize source node
    s.dist = len(graph.nodes())
    # populate edges going out of the source node
    for edge in s.outgoing_edges():
        edge.load = edge.capacity
        edge.destination().overrun = edge.load
        edge.destination().edge_to(s).load = -edge.capacity

    # 
    # solve the max flow problem
    #
    while _has_active_node(graph, s, t):
        node = _get_active_node(graph, s, t)
        if not _push(node):
            _relabel(node)
            print("relabeling %s to dist %i" % (node.name(), node.dist))

    # cleanup
    for edge in graph.edges():
        if hasattr(edge, "tmp"):
            graph.remove_edge(edge)
