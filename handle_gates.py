import osmium

import osmium_extract
from functions import read_from_pkl, write_to_pkl
from node import Node

GATE_FILTER = [
    "n/locked=yes",
    "n/access=private",
]


class GateHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.gates = set()

    def node(self, n):
        self.gates.add(Node(n.id, n.location.lat, n.location.lon))


def make_pkl(project):
    "Read locked gates and other obstructions."
    osmium_extract.extract_tags(
        project.area_pbf, project.gates_osm, GATE_FILTER
    )
    handler = GateHandler()
    handler.apply_file(project.gates_osm, locations=True)
    write_to_pkl(project.gates_pkl, handler.gates)


def get_gates(project):
    return read_from_pkl(project.gates_pkl)
