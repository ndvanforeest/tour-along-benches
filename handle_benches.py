import osmium

import osmium_extract
from functions import read_from_pkl, write_to_pkl
from node import Node

BENCH_FILTER = [
    "n/amenity=bench",
]


class BenchHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.benches = []

    def node(self, n):
        # The BENCH_OSM_FILE only contains benches, hence, the commented
        # check is not necessary.
        # if "amenity" in n.tags and n.tags["amenity"] == "bench":
        self.benches.append(Node(n.id, n.location.lat, n.location.lon))


def make_pkl(project):
    "Read benches from osm, write to pickle file."
    osmium_extract.extract_tags(
        project.area_pbf, project.benches_osm, BENCH_FILTER
    )
    handler = BenchHandler()
    handler.apply_file(project.benches_osm, locations=True)

    write_to_pkl(project.benches_pkl, handler.benches)


def get_benches(project):
    return read_from_pkl(project.benches_pkl)
