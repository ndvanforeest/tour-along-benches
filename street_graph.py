from functools import cache
import igraph

from node import Node


class Graph:
    def __init__(
        self,
        nodes: list[Node] = [],
        edges: list[list[Node, Node]] = [],
    ):
        self.__n2p = {}  # maps name to node
        self._b2v = {}  # maps bench to vertex
        self._g = igraph.Graph()
        for node in nodes:
            self.add_vertex(node)
        self.add_edges(edges)

    def contains(self, node):
        return node.name in self.__n2p

    def add_vertex(self, node):
        if not self.contains(node):
            self._g.add_vertex(name=node.name)
            self.__n2p[node.name] = node

    def add_edge(self, p: Node, q: Node):
        if not self.contains(p):
            self.add_vertex(p)
        if not self.contains(q):
            self.add_vertex(q)
        self._g.add_edge(self._p2i(p), self._p2i(q))

    def add_edges(self, edges: list[list[Node, Node]]):
        # Don't add edges separately, this gives a huge performance penalty
        self._g.add_edges([e[0].name, e[1].name] for e in edges)

    def _i2n(self, idx):
        "map index to name"
        return self._g.vs[idx]["name"]

    def _i2p(self, idx):
        "map index to node"
        return self._n2p(self._i2n(idx))

    def _n2p(self, name):
        "map name to node"
        return self.__n2p[name]

    def _p2i(self, node):
        "map node to index"
        return self._g.vs.find(name=node.name).index

    def vertices(self):
        return list(self.__n2p.values())

    @cache
    def edges(self):
        return list(
            (self._i2p(e.source), self._i2p(e.target)) for e in self._g.es
        )

    def delete_vertices(self, nodes: list[Node]):
        self._g.delete_vertices(
            [self._p2i(p) for p in nodes if p.name in self.__n2p]
        )
        for p in nodes:
            self.__n2p.pop(p.name, None)

    def delete_edges(self, edges):
        edges = [(self._p2i(e[0]), self._p2i(e[1])) for e in edges]
        self._g.delete_edges(edges)

    def neighbors(self, node):
        return [self._i2p(i) for i in self._g.neighbors(self._p2i(node))]

    def giant(self):
        components = self._g.connected_components(mode="weak")
        giant = components.giant()
        nodes = [self._n2p(name) for name in giant.vs["name"]]
        edges = [
            [
                self._n2p(giant.vs[edge.source]["name"]),
                self._n2p(giant.vs[edge.target]["name"]),
            ]
            for edge in giant.es
        ]
        return Graph(nodes, edges)

    def vcount(self):
        return self._g.vcount()

    def ecount(self):
        return self._g.ecount()

    def get_shortest_path(self, source, target):
        s = self._p2i(source)
        t = self._p2i(target)
        path = self._g.get_shortest_path(s, to=t)  # , weights='length')
        return [self._i2p(idx) for idx in path]

    def get_shortest_paths(self, source, targets):
        s = self._p2i(source)
        t_idxs = [self._p2i(t) for t in targets]
        paths = self._g.get_shortest_paths(s, to=t_idxs, weights="length")
        return [[self._i2p(idx) for idx in path] for path in paths]

    def osm2node(self, name):
        return self._n2p(name)

    def compute_edge_lengths(self):
        from geopy.distance import geodesic

        lengths = []
        for e in self._g.es:
            dist = geodesic(self._i2p(e.source).gps, self._i2p(e.target).gps)
            lengths.append(int(dist.meters))
        self._g.es["length"] = lengths

    def distances(self, sources, targets):
        sources = [self._p2i(s) for s in sources]
        targets = [self._p2i(t) for t in targets]
        return self._g.distances(sources, targets, weights="length")

    def names(self):
        return self._g.vs["name"]

    def set_bench_name(self, bench, node):
        self._b2v[bench] = node

    def bench2vertex(self, bench):
        return self._b2v[bench]
