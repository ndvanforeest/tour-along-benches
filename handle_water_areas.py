import osmium
from shapely import Polygon

import osmium_extract
from functions import read_from_pkl, write_to_pkl
from node import Node

WATER_FILTER = [
    "natural=water",
    "waterway=riverbank",
    "landuse=reservoir",
    "landuse=basin",
]


class WaterHandler(osmium.SimpleHandler):
    "Water areas are outer rings,  islands or islets are inner rings."

    def __init__(self):
        super().__init__()
        self.areas = []

    def area(self, a):
        is_water = False
        for tag in a.tags:
            if tag.k == "natural" and tag.v == "water":
                is_water = True

        if is_water:
            for outer_ring in a.outer_rings():
                outer_nodes = [Node(n.ref, n.lat, n.lon) for n in outer_ring]
                inner_rings = []
                for inner_ring in a.inner_rings(outer_ring):
                    inner_nodes = [
                        Node(n.ref, n.lat, n.lon) for n in inner_ring
                    ]
                    inner_rings.append(inner_nodes)
                self.areas.append([outer_nodes, inner_rings])


def convert_area_to_polygon(areas):
    "Convert water area to shapely polygon with holes for islands."
    water_polygons = []
    for outer_ring, inner_rings in areas:
        out = [n.gps for n in outer_ring]
        inners = [[n.gps for n in ir] for ir in inner_rings]
        water_polygons.append(Polygon(out, holes=inners))
    return water_polygons


def make_pkl(project):
    "Read water areas from osm, write to pickle."
    osmium_extract.extract_tags(
        project.area_pbf, project.water_areas_osm, WATER_FILTER
    )
    handler = WaterHandler()
    handler.apply_file(project.water_areas_osm, locations=True)
    write_to_pkl(project.water_areas_pkl, handler.areas)


def get_water_areas(project):
    return read_from_pkl(project.water_areas_pkl)
