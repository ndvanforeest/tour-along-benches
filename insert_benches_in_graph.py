from collections import defaultdict
from itertools import pairwise

from shapely.geometry import LineString
from shapely.ops import nearest_points
from shapely.strtree import STRtree

import handle_benches
import handle_graph
import handle_water_areas
from node import Node, point_to_node
from street_graph import Graph


def nearest_node_on_edge(node, edge):
    "Find node on  edge that is closest to node."
    m, n = edge
    segment = LineString((m.p, n.p))
    dist_to_seg = node.p.distance(segment) + 1e-8  # add rounding error
    if node.p.distance(m.p) <= dist_to_seg:
        return m
    if node.p.distance(n.p) <= dist_to_seg:
        return n
    return point_to_node(nearest_points(node.p, segment)[1])


def edge_to_linestring(edge):
    "Make edge suitable for analysis with Shapely"
    return LineString((edge[0].p, edge[1].p))


def is_dry_path(p, q, water_polygons):
    "True if the segment between p and q does not cuts a water polygon"
    return not any(LineString((p, q)).intersects(water_polygons))


def is_dry_to_edge(node, edge, water_polygons):
    "True if there's a dry path from node to edge"
    np = nearest_node_on_edge(node, edge)
    return is_dry_path(node.p, np.p, water_polygons)


def reachable_edge_and_node(node: Node, rtree: STRtree, edges, water_polygons):
    "Find edge and node that are reachable from the given node"
    nearest_edge = edges[rtree.nearest(node.p)]
    if is_dry_to_edge(node, nearest_edge, water_polygons):
        nearest_point = nearest_node_on_edge(node, nearest_edge)
        return nearest_point, nearest_edge
    delta = 3 * node.p.distance(edge_to_linestring(nearest_edge))
    idxs = rtree.query(node.p.buffer(delta))
    good_edges = [
        edges[idx]
        for idx in idxs
        if is_dry_to_edge(node, edges[idx], water_polygons)
    ]
    if good_edges:
        nearest_edge = min(
            good_edges,
            key=lambda edge: node.p.distance(edge_to_linestring(edge)),
        )
    # Give up, the bench can be in the middle of a small lake.
    print(f"Nothing worked: There are no good edges for bench {node}")
    nearest_point = nearest_node_on_edge(node, nearest_edge)
    return nearest_point, nearest_edge


def insert_bench_vertices(g: Graph, benches, water_areas):
    "Add vertices to graph reachable from the benches."
    water_polygons = handle_water_areas.convert_area_to_polygon(water_areas)
    segments = [LineString((p.gps, q.gps)) for p, q in g.edges()]
    rtree = STRtree(segments)
    edges_to_add = defaultdict(list)
    bench_node_edges = []
    for bench in benches:
        node, edge = reachable_edge_and_node(
            bench, rtree, g.edges(), water_polygons
        )
        if not g.contains(node):
            edges_to_add[edge].append(bench)
        bench_node_edges.append((bench, node))
        g.add_edge(bench, node)
        g.set_bench_name(bench, node)
    for edge in edges_to_add.keys():
        new_vertices = edges_to_add[edge]
        new_edges = sorted(
            list(g.bench2vertex(bench) for bench in new_vertices)
            + list(edge[:])
        )
        g.add_edges([(m, n) for m, n in pairwise(new_edges)])
    g.delete_edges(edges_to_add.keys())


def make_pkl(project):
    "Add the benches as vertices to the graph and save result."
    benches = handle_benches.get_benches(project)
    g = handle_graph.get_graph(project)
    water_areas = handle_water_areas.get_water_areas(project)

    insert_bench_vertices(g, benches, water_areas)

    handle_graph.write_to_pkl(project.graph_pkl, g)
