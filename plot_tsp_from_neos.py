import webbrowser
from itertools import pairwise

from folium import CircleMarker, Map, PolyLine
from folium.plugins import PolyLineOffset

import handle_benches
import handle_graph
from node import find_center
from run_scenario import project

g = handle_graph.get_graph(project)
benches = handle_benches.get_benches(project)


def read_neos_file():
    with open(project.tour_file, "r") as fp:
        line = fp.readline()  # skip line
        while "Number of Nodes:" not in line:
            line = fp.readline()
        _, dim = line.split(":")
        dim = int(dim)
        idx2name = {}
        line = fp.readline()  # skip line
        for num in range(dim):
            line = fp.readline()
            idx, name, lat, lon = line.split()
            idx2name[int(idx)] = name.strip()
        while f"{dim} {dim}" not in line:
            line = fp.readline()
        tour = [idx2name[0]]
        for num in range(dim):
            line = fp.readline()
            m, n, _ = line.split()
            tour.append(idx2name[int(n)])
        return convert_to_node(tour)


def convert_to_node(tour):
    "Convert list of node ids to list of nodes."
    return [g.osm2node(n) for n in tour]


def plot_tour(tour):
    center = find_center(tour)
    html_file = f"/home/nicky/tmp/html_files/{project.name}_tour.html"
    map = Map(location=center.gps, zoom_start=15)
    for s, t in pairwise(tour):
        path = [p.gps for p in g.get_shortest_path(s, t)]
        PolyLineOffset(path, offset=4.5).add_to(map)
        PolyLine(path, color="red", weight=3, opacity=1).add_to(map)
    for bench in benches:
        CircleMarker(
            location=bench.gps, popup=bench.name, radius=3, color="blue"
        ).add_to(map)
        CircleMarker(
            location=g.bench2vertex(bench).gps, radius=3, color="red"
        ).add_to(map)
    # lines between vertex and bench
    for bench in benches:
        PolyLine(
            [bench.gps, g.bench2vertex(bench).gps],
            color="black",
            weight=2.5,
        ).add_to(map)
    map.save(html_file)
    webbrowser.get("firefox").open_new_tab(f"file://{html_file}")


def export_to_gps(tour):
    import gpxpy

    gpx = gpxpy.gpx.GPX()

    # You can add markers for each street point nearest
    # to a bench
    # for point in tsp:
    #     gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(*point.gps))

    # add the tracks
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx_track.name = project.name
    gpx.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    for s, t in pairwise(tour):
        path = g.get_shortest_path(s, t)
        for point in path:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(*point.gps))
    with open(project.gpx_file, "w") as fp:
        fp.write(gpx.to_xml())


if __name__ == "__main__":
    tour = read_neos_file()
    plot_tour(tour)
    # export_to_gps(tour)
