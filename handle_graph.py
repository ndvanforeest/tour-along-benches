from itertools import pairwise

import handle_gates
import handle_streets
from functions import read_from_pkl, write_to_pkl
from street_graph import Graph


def make_graph(project):
    "The largest component of the graph of streets."
    streets = handle_streets.get_streets(project)

    g = Graph()
    # It's faster to add the vertices separately first.
    # And, it's much faster to add the edges as a  large list
    edges = []
    for street in streets:
        for point in street:
            g.add_vertex(point)
        edges += list((m, n) for m, n in pairwise(street))
    g.add_edges(edges)

    gates = handle_gates.get_gates(project)
    g.delete_vertices(gates)
    g = g.giant()
    write_graph(g, project)


def compute_lengths(project):
    "Compute the length of all edges."
    g = get_graph(project)
    g.compute_edge_lengths()
    write_graph(g, project)


def write_graph(g, project):
    write_to_pkl(project.graph_pkl, g)


def get_graph(project):
    return read_from_pkl(project.graph_pkl)
