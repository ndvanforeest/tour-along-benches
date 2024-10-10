"""
Compute a good tour with 2opt. The ideas are based on the ipynb file of Peter Norvig
on tsps.
"""

from functools import cache
from itertools import pairwise

import numpy as np

from scenario import Scenario


City = int  # e.g. City(300, 100)
Cities = frozenset  # A set of cities
Tour = list  # A list of cities visited, in order


def read_tsplib(fname: str):
    "Read nodes and distances from tsplib file."
    with open(fname, "r", encoding="utf-8") as fp:
        line = fp.readline()
        while "DIMENSION" not in line:
            line = fp.readline()
        _, dim = line.split()
        dim = int(dim)
        distances = np.zeros((dim, dim), dtype=int)
        while "COMMENT" not in line:
            line = fp.readline()
        idx2name = {}
        for num in range(dim):
            _, idx, name, gps = line.split(":")
            idx2name[int(idx)] = name.strip()
            line = fp.readline()
        while "EDGE_WEIGHT_SECTION" not in line:
            line = fp.readline()
        for num in range(dim):
            line = fp.readline()
            distances[num, :] = [int(d) for d in line.split()]
        return distances, idx2name


def first(collection):
    """The first element of a collection."""
    return next(iter(collection))


def nearest_neighbor(A: City, cities, distances) -> City:
    """Find the city C in cities that is nearest to city A."""
    return min(cities, key=lambda C: distances[C, A])


def nearest_tsp(distances, start=None) -> Tour:
    """Create a partial tour that initially is just the start city.
    At each step extend the partial tour to the nearest unvisited neighbor
    of the last city in the partial tour, while there are unvisited cities remaining.
    """
    cities = range(distances.shape[0])
    start = start or first(cities)
    tour = [start]
    unvisited = set(cities) - {start}

    def extend_to(C):
        tour.append(C)
        unvisited.remove(C)

    while unvisited:
        extend_to(nearest_neighbor(tour[-1], unvisited, distances))
    return tour


def opt2(tour, distances) -> Tour:
    "Perform 2-opt segment reversals to optimize tour."
    changed = False
    for i, j in subsegments(len(tour)):
        if reversal_is_improvement(tour, i, j, distances):
            tour[i:j] = reversed(tour[i:j])
            changed = True
    return tour if not changed else opt2(tour, distances)


def reversal_is_improvement(tour, i, j, distances) -> bool:
    "Would reversing the segment `tour[i:j]` make the tour shorter?"
    # Given tour [...A,B--C,D...], would reversing B--C make the tour shorter?
    A, B, C, D = tour[i - 1], tour[i], tour[j - 1], tour[j % len(tour)]
    return (
        distances[A, B] + distances[C, D] > distances[A, C] + distances[B, D]
    )


@cache  # All tours of length N have the same subsegments, so cache them.
def subsegments(N) -> tuple[tuple[int, int]]:
    "Return (i, j) index pairs denoting tour[i:j] subsegments of a tour of length N."
    return tuple(
        (i, i + length)
        for length in reversed(range(2, N - 1))
        for i in range(N - length)
    )


def tour_length(tour: Tour, distances) -> float:
    "The total distances of each link in the tour, including the link from last back to first."
    return sum(distances[tour[i], tour[i - 1]] for i in range(len(tour)))


def write_tour(tour: Tour, idx2name, fname):
    "Write the tour to neos output format."
    with open(fname, "w") as fp:
        fp.write(f"Number of Nodes: {len(tour)}\n")
        fp.write("Explicit Length\n")
        for k, v in idx2name.items():
            fp.write(f"{k} {v} (53.1, 6.56)\n")
        fp.write(f"{len(tour)} {len(tour)}\n")
        for m, n in pairwise(tour):
            fp.write(f"{m} {n} 0\n")
        fp.write(f"{tour[-1]} {tour[0]} 0\n")


def make_tour(project: Scenario):
    distances, idx2name = read_tsplib(project.tsplib_file)
    tour = nearest_tsp(distances)
    print("tour length nearest neighbor: ", tour_length(tour, distances))
    tour = opt2(tour, distances)
    print("tour lenght after 2 opt: ", tour_length(tour, distances))
    write_tour(tour, idx2name, project.tour_file)
