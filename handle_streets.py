import osmium

import osmium_extract
from functions import read_from_pkl, write_to_pkl
from node import Node

STREET_FILTER = [
    "nw/bicycle=yes",
    "nw/bicycle=use_sidepath",
    "nw/cycleway:both",
    "nw/foot=use_sidepath",
    "nw/highway=bridleway",
    "nw/highway=cycleway",
    "nw/highway=footway",
    "nw/highway=path",
    "nw/highway=living_street",
    "nw/highway=pedestrian",
    "nw/highway=residential",
    "nw/highway=service",
    "nw/highway=steps",
    "nw/highway=tertiary",
    "nw/highway=track",
    "nw/highway=unclassified",
    "nw/sidewalk=both",
    "nw/sidewalk=left",
    "nw/sidewalk=right",
]


class StreetHandler(osmium.SimpleHandler):
    "The streets are filtered from the osm."

    def __init__(self):
        super().__init__()
        self.streets = []

    def way(self, w):
        self.streets.append(
            [Node(ref=n.ref, lat=n.lat, lon=n.lon) for n in w.nodes]
        )


def make_pkl(project):
    osmium_extract.extract_tags(
        project.area_pbf, project.streets_osm, STREET_FILTER
    )
    handler = StreetHandler()
    handler.apply_file(project.streets_osm, locations=True)
    write_to_pkl(project.streets_pkl, handler.streets)


def get_streets(project):
    return read_from_pkl(project.streets_pkl)
