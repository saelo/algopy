#coding: UTF-8
#
# Implementation of the cycle cancelling algorithm to solve the min cost flow problem.
#
# Copyright (c) 2013 Samuel Groß
#

from graph import *
from max_flow import solve_max_flow
from copy import deepcopy
from bellman_ford import bellman_ford_cycle


def _build_residual_graph(graph):
    res = deepcopy(graph)

    for edge in res.edges():
        if edge.load > 0:
            if res.has_reverse_edge(edge):
                raise ValueError("reverse edge found, something is wrong")
            else:
                print("[*] adding reverse edge %s --> %s" % (edge.destination().name(), edge.source().name()))
                res.add_edge(edge.destination(), edge.source(), {"capacity" : edge.load,
                                                                 "load" : 0,
                                                                 "cost" : -edge.cost})
            edge.capacity -= edge.load
        if edge.capacity == 0:
            print("[*] removing edge %s --> %s" % (edge.source().name(), edge.destination().name()))
            res.remove_edge(edge)

    return res


def _stats(g):
    costs = 0
    load = 0
    for edge in g.edges():
        costs += edge.load * edge.cost
        load += edge.load
   
    return (load, costs)


def is_valid_flow(graph):
    """
    Returns true if the graph contains a valid flow.
    """
    for node in graph.nodes():
        if hasattr(node, "demand"):
            flow = node.demand
        else:
            flow = 0
        for edge in node.outgoing_edges():
            flow += edge.load
        for edge in node.incoming_edges():
            flow -= edge.load

        if not flow == 0:
            return False

    return True


def solve_min_cost_flow(graph):
    """
    Solves the min cost flow problem using the cycle cancelling algorithm.
    """
    #
    # initialize algorithm specific data
    #
    # add two temporary nodes: global source and global target
    gs, gt = graph.add_nodes(["GS", "GT"])

    # connect producers to global source and consumers to global target
    for node in graph.nodes():
        if not node is gs and not node is gt:
            if node.demand < 0:
                graph.add_edge(gs, node, {"capacity" : -node.demand})
            elif node.demand > 0:
                graph.add_edge(node, gt, {"capacity" : node.demand})

    # 
    # solve the min cost flow problem
    #
    # first calculate a valid path by solving the max-flow problem
    solve_max_flow(graph, gs, gt)

    # remove temporary nodes
    graph.remove_nodes(["GS", "GT"])
    print("[*] done calculating the maximum flow")
    print("[*] total load: %i total costs: %i" % _stats(graph))

    #
    # improve the flow:
    # build the residual graph and determine negative cost cycles
    repeat = True
    while repeat:
        res_graph = _build_residual_graph(graph)
        repeat = False

        neg_cycle = bellman_ford_cycle(res_graph)
        if neg_cycle:
            print("[*] negative cost cycle found, adapting flow...")
            max_flow = None
            for edge in neg_cycle.edges():
                if max_flow is None or edge.capacity < max_flow:
                    max_flow = edge.capacity

            repeat = True
            for edge in neg_cycle.edges():
                # need to use names here as we are working on a deep copy of the original graph
                n_edge = graph.get_edge(edge.source().name(), edge.destination().name())
                if n_edge is None:
                    graph.get_edge(edge.destination().name(), edge.source().name()).load -= max_flow
                else:
                    n_edge.load += max_flow

                      
    print("[*] no (more) negative cost cycles, done.")
    print("[*] total load: %i total costs: %i" % _stats(graph))
