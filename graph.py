#!/usr/bin/env python
#coding: UTF-8
#
# Classes to represent graphs
#
# Copyright (c) 2013 Samuel Groß
#


class Graph:
    """
    Represents a graph.
    """

    def __init__(self):
        self._nodes = {}
        self._edges = []


    def nodes(self):
        """
        Returns all nodes in this graph.
        """
        return list(self._nodes.values())

    def edges(self):
        """
        Returns all edges in this graph.
        """
        return list(self._edges)

    def add_node(self, name, data = None):
        """
        Add a node to the graph.

        If no node with the given name already exists a new one is created
        and the node object is returned to the caller.
        """
        if self.has_node(name):
            raise ValueError("Node %s already exists" % name)
        self._nodes[name] = Node(name, data if data is not None else {})
        return self._nodes[name]

    def add_nodes(self, l):
        """
        Add multiple nodes, returns a list of the created node objects.
        """
        ret = []
        for name in l:
            ret.append(self.add_node(name))
        return ret

    def remove_node(self, n):
        """
        Remove the given node from this graph
        """
        node = self._node_lookup([n])
        del self._nodes[node.name()]

    def remove_nodes(self, l):
        """
        Remove every node in the given list of node names.
        """
        for nodename in l:
            self.remove_node(nodename)

    def add_edge(self, src, dst, data = None):
        """
        Add a (directed) edge between two nodes.

        Returns the edge object on success.
        """
        srcnode, dstnode = self._node_lookup([src, dst])
        if srcnode is None or dstnode is None:
            raise ValueError("No such node in this graph")
        edge = Edge(srcnode, dstnode, data if data is not None else {})
        self._edges.append(edge)
        srcnode._add_outgoing_edge(edge)
        dstnode._add_incoming_edge(edge)
        return edge

    def remove_edge(self, edge):
        """
        Removes the given edge from this graph.
        """
        if not edge in self._edges:
            return
        self._edges.remove(edge)
        edge.source()._remove_outgoing_edge(edge)
        edge.destination()._remove_incoming_edge(edge)

    def remove_edges(self, l):
        """
        Removes all edges in the given list
        """
        for edge in l:
            self.remove_edge(l)

    def get_node(self, name):
        """
        Returns the node object with the given name or None if there is no such node.
        """
        return self._nodes.get(name, None)

    def has_node(self, name):
        """
        Returns true if a node with the given name exists in this graph.
        """
        return name in self._nodes

    def get_edge(self, n1, n2):
        """
        Returns the edge from the first to the second node or None if there is no such edge.
        """
        src, dst = self._node_lookup([n1, n2])
        if src is None or dst is None:
            raise ValueError("No such node in this graph")
        return src.edge_to(dst)

    def has_edge(self, n1, n2):
        """
        Returns true if there is an edge from the first to the second node in this graph.
        """
        return self.get_edge(n1, n2) is not None

    def get_reverse_edge(self, edge):
        """
        Returns the inverse edge to the given edge or None if there is no such edge.
        """
        return edge.destination().edge_to(edge.source())

    def has_reverse_edge(self, edge):
        """
        Returns true if an inverse edge to the given edge exists in this graph.
        """
        return self.get_reverse_edge(edge) is not None

    def clear(self):
        """
        Removes all nodes and edges from this graph.
        """
        self._nodes = {}
        self._edges = []

    def reset(self):
        """
        Removes all custom attributes from the graphs nodes and edges.
        """
        for edge in self.edges():
            edge.clear()
        for node in self.nodes():
            node.clear()

    def _node_lookup(self, l):
        """
        Returns the node objects represented by the elements of the given list.

        The list can contain node IDs or node objects directly, the resulting list will
        only contain valid node objects or None if there was no valid node object.
        """
        res = []
        for obj in l:
            if obj in self.nodes():
                res.append(obj)
            else:
                res.append(self._nodes.get(obj, None))

        return res

    def __str__(self):
        res = "Nodes:\n"
        for node in self._nodes.values():
            res += str(node)

        res += "Edges:\n"
        for edge in self._edges:
            res += str(edge)

        return res


class Node:
    """
    Represents a node in a graph.
    """

    def __init__(self, name, data = None):
        self._name = name
        self._outgoing_edges = {}
        self._incoming_edges = {}
        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)

    def _add_outgoing_edge(self, edge):
        self._outgoing_edges[edge.destination()] = edge

    def _add_incoming_edge(self, edge):
        self._incoming_edges[edge.source()] = edge

    def _remove_outgoing_edge(self, edge):
        del self._outgoing_edges[edge.destination()]

    def _remove_incoming_edge(self, edge):
        del self._incoming_edges[edge.source()]

    def name(self):
        """
        Returns the name of this node.
        """
        return self._name

    def outgoing_edges(self):
        """
        Returns a list of edges going out of this node.
        """
        return list(self._outgoing_edges.values())

    def incoming_edges(self):
        """
        Returns a list of edges going into this node.
        """
        return list(self._incoming_edges.values())

    def edge_to(self, node):
        """
        If available returns an edge from this node
        to the given node else None.
        """
        return self._outgoing_edges.get(node, None)

    def edge_from(self, node):
        """
        If available returns an edge from the given
        node to this node else None.
        """
        return self._incoming_edges.get(node, None)

    def has_edge_to(self, node):
        """
        Returns true if there is an edge from this
        node to the given one.
        """
        return self.edge_to(node) is not None

    def has_edge_from(self, node):
        """
        Returns true if there is an edge from the
        given node to this one.
        """
        return self.edge_from(node) is not None

    def clear(self):
        """
        Removes all custom attributes from this node.
        """
        for key, value in vars(self).items():
            if not key.startswith("_"):
                delattr(self, key)

    def __str__(self):
        res = self._name + "\n"
        for key, value in vars(self).items():
            if not key.startswith("_"):
                res += "    " + str(key) + " : " + str(value) + "\n"

        return res


class Edge:
    """
    Represents an edge between two nodes in a graph.
    """

    def __init__(self, node1, node2, data = None):
        self._is_directed = True
        self._node1  = node1
        self._node2  = node2
        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)

    def source(self):
        """
        Returns the source node of this edge.
        """
        return self._node1

    def destination(self):
        """
        Returns the destination node of this edge.
        """
        return self._node2

    def is_directed(self):
        """
        Returns true if this is a directed edge.
        """
        return self._is_directed

    def clear(self):
        """
        Removes all custom attributes from this edge.
        """
        for key, value in vars(self).items():
            if not key.startswith("_"):
                delattr(self, key)

    def __str__(self):
        res = self._node1.name() + " --> " + self._node2.name() + "\n"
        for key, value in vars(self).items():
            if not key.startswith("_"):
                res += "    " + str(key) + " : " + str(value) + "\n"

        return res

class Path:
    """
    Represents a path between two nodes.
    """

    def __init__(self, start):
        self._nodes = [start]
        self._edges = []

    def nodes(self):
        """
        Returns an ordered list of nodes in this path.

        The first element is the starting node in this path.
        """
        return list(self._nodes)

    def edges(self):
        """
        Returns an ordered list of edges in this path.

        The first element in the list is the edge from the start node
        to its sucessor.
        """
        return list(self._edges)

    def start(self):
        """
        Returns the first node in this path.
        """
        return self._nodes[0]

    def end(self):
        """
        Returns the last node in this path.
        """
        return self._nodes[-1]

    def append(self, edge, node):
        """
        Adds a new node and the corresponding edge to this path.
        """
        if not edge.source() == self._nodes[-1] or not edge.destination() == node:
            raise ValueError("Edge is not connecting the new and the previous node")
        self._nodes.append(node)
        self._edges.append(edge)

    def pop(self):
        """
        Removes the last (edge, node) pair added to this path.
        """
        self._nodes.pop()
        self._edges.pop()
