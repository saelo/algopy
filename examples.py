#!/usr/bin/env python
#coding: UTF-8
#
# Examples.
#
# Copyright (c) 2013 Samuel Groß
#

from graph import *
from basics import *
from max_flow import solve_max_flow


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

if __name__ == "__main__":
    max_flow()
