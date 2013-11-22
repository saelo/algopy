#!/usr/bin/env python
#coding: UTF-8
#
# Examples.
#
# Copyright (c) 2013 Samuel Groß
#

from graph import *
from algorithms.basics import *
from algorithms.max_flow import solve_max_flow
from algorithms.min_cost_flow import solve_min_cost_flow
from algorithms.min_cut import solve_min_cut


def max_flow():
    g = Graph()
    g.add_nodes(["S", "A", "B", "C", "D", "E", "F", "T"])
    g.add_edge("S", "A", {"capacity" : 38})
    g.add_edge("S", "B", {"capacity" : 1})
    g.add_edge("S", "F", {"capacity" : 2})
    g.add_edge("A", "B", {"capacity" : 8})
    g.add_edge("A", "C", {"capacity" : 10})
    g.add_edge("A", "D", {"capacity" : 13})
    g.add_edge("B", "C", {"capacity" : 26})
    g.add_edge("C", "E", {"capacity" : 8})
    g.add_edge("C", "F", {"capacity" : 24})
    g.add_edge("C", "T", {"capacity" : 1})
    g.add_edge("D", "B", {"capacity" : 2})
    g.add_edge("D", "E", {"capacity" : 1})
    g.add_edge("D", "T", {"capacity" : 7})
    g.add_edge("E", "T", {"capacity" : 7})
    g.add_edge("F", "T", {"capacity" : 27})

    solve_max_flow(g, g.get_node("S"), g.get_node("T"))
    print(g)

def min_cost():
    g = Graph()
    g.add_node("A", {"demand" : -4})
    g.add_node("B", {"demand" : -7})
    g.add_node("C", {"demand" :  0})
    g.add_node("D", {"demand" :  2})
    g.add_node("E", {"demand" :  0})
    g.add_node("F", {"demand" :  0})
    g.add_node("G", {"demand" :  5})
    g.add_node("H", {"demand" :  4})
    g.add_edge("A", "B", {"capacity" : 4, "cost" : 1})
    g.add_edge("A", "C", {"capacity" : 3, "cost" : 2})
    g.add_edge("B", "D", {"capacity" : 9, "cost" : 3})
    g.add_edge("D", "C", {"capacity" : 5, "cost" : 5})
    g.add_edge("D", "F", {"capacity" : 8, "cost" : 1})
    g.add_edge("C", "E", {"capacity" : 3, "cost" : 2})
    g.add_edge("E", "F", {"capacity" : 1, "cost" : 4})
    g.add_edge("F", "H", {"capacity" : 9, "cost" : 0})
    g.add_edge("E", "G", {"capacity" : 2, "cost" : 2})
    g.add_edge("H", "G", {"capacity" : 6, "cost" : 1})

    print(g)
    solve_min_cost_flow(g)
    print(g)

def min_cut():
    g = Graph()
    g.add_nodes(["A", "B", "C", "D", "E"])
    g.add_undirected_edge("A", "B", {"weight": 3})
    g.add_undirected_edge("A", "C", {"weight": 1})
    g.add_undirected_edge("B", "C", {"weight": 1})
    g.add_undirected_edge("B", "D", {"weight": 2})
    g.add_undirected_edge("B", "E", {"weight": 3})
    g.add_undirected_edge("C", "D", {"weight": 2})
    g.add_undirected_edge("D", "E", {"weight": 1})

    solve_min_cut(g)

if __name__ == "__main__":
    print("=====================================")
    print("max flow")
    print("=====================================")
    max_flow()

    print("=====================================")
    print("min cost flow")
    print("=====================================")
    min_cost() 

    print("=====================================")
    print("min cut")
    print("=====================================")
    min_cut() 
