#!/usr/bin/env python
#coding: UTF-8
#
# Implementation of the Stoer-Wagner algorithm to solve the minimum cut problem.
#
# Copyright (c) 2013 Samuel Groß
#

import sys
from graph import *
from copy import deepcopy

def merge(graph, node1, node2):
    """
    Merges the two given nodes into one node and returns a copy of
    the old graph with the two nodes merged together.
    """
    new = deepcopy(graph)
    merged = new.add_node(node1.name() + node2.name())

    for edge in node1.outgoing_edges() + node2.outgoing_edges():
        other = edge.node1() if not edge.node1() == node1 and not edge.node1() == node2 else edge.node2()
        if not new.has_edge(merged, other.name()):
            new.add_undirected_edge(merged, other.name(), {"weight" : edge.weight})
        else:
            new.get_edge(merged, other.name()).weight += edge.weight

    new.remove_nodes([node1.name(), node2.name()])

    return new

def get_strongly_connected_node(graph, nodeset):
    """
    Returns the node connected to the given node set the strongest.

    Returns None if there are no more nodes left.
    """
    max_weight = 0
    res = None
    for node in graph.nodes():
        if node not in nodeset:
            cur_weight = 0
            for other in nodeset:
                if other.has_edge_to(node):
                    cur_weight += other.edge_to(node).weight
            if cur_weight > max_weight:
                max_weight = cur_weight
                res = node

    return res

def solve_min_cut(graph):
    """
    Calculate a minimum cut in the given graph.
    """
    if not graph.is_undirected():
        raise ValueError("graph must be undirected")

    min_cut = sys.maxsize
    phase = 1
    while True:
        nodeset = [graph.nodes()[0]]
        while len(nodeset) < len(graph.nodes()) - 1:
            nodeset.append(get_strongly_connected_node(graph, nodeset))

        last_node = get_strongly_connected_node(graph, nodeset)
        cut = 0
        for edge in last_node.outgoing_edges():
            cut += edge.weight

        graph = merge(graph, nodeset[-1], last_node)
        print("[*] result from phase %i: %i" % (phase, cut))
        phase += 1
        if cut < min_cut:
            min_cut = cut

        if len(graph.nodes()) == 1:
            break

    print("[*] minimun cut found: %i" % min_cut)
