from functools import cache
from statistics import mean

import numpy as np
from geopy.distance import geodesic
from shapely import Point


class Node:
    __slots__ = ["ref", "lat", "lon"]

    def __init__(self, ref: int, lat: float, lon: float):
        self.ref = ref
        self.lat = lat
        self.lon = lon

    def __getstate__(self):
        return (self.ref, self.lat, self.lon)

    def __setstate__(self, state):
        self.ref, self.lat, self.lon = state

    @property
    def gps(self):
        return (self.lat, self.lon)

    @property
    def name(self):
        return str(self.ref)

    def __repr__(self):
        return f"{self.ref:>16}: {self.lat:>9.7f}, {self.lon:>9.7f}"

    def distance(self, p):
        return geodesic(self.gps, p.gps).meters

    @property
    def radians(self):
        return np.radians(self.gps)

    @property
    @cache
    def p(self):
        return Point(self.gps)

    def __hash__(self):
        return self.ref

    def __eq__(self, o):
        return self.ref == o.ref

    def __lt__(self, other):
        if self.lat != other.lat:
            return self.lat < other.lat
        else:
            return self.lon < other.lon


def gps_to_node(lat, lon):
    ref = int((lat + lon) * 1e7) * 100000  # hopefully unique
    return Node(ref, lat, lon)


def point_to_node(point: Point):
    lat, lon = point.coords[0]
    return gps_to_node(lat, lon)


def find_center(nodes):
    mean_lat = mean(n.lat for n in nodes)
    mean_lon = mean(n.lon for n in nodes)
    return gps_to_node(mean_lat, mean_lon)
