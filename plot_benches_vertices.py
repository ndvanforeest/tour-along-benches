#!/usr/bin/env python
"""Plot benches and closest street vertices."""

import webbrowser
from statistics import mean

import folium

import handle_benches
import handle_graph
from run_scenario import project

benches = handle_benches.get_benches(project)
g = handle_graph.get_graph(project)

mean_lat = mean(b.lat for b in benches)
mean_lon = mean(b.lon for b in benches)


html_file = f"/home/nicky/tmp/html_files/{project.name}_b2v.html"

m = folium.Map(location=(mean_lat, mean_lon), zoom_start=16)
for bench in benches:
    folium.CircleMarker(
        location=bench.gps,
        radius=9,
        color="blue",
    ).add_to(m)
    vertex = g.bench2vertex(bench)
    folium.CircleMarker(
        location=vertex.gps,
        radius=3,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=1,
    ).add_to(m)
    folium.PolyLine(
        [bench.gps, vertex.gps], color="black", weight=2.5, opacity=1
    ).add_to(m)
m.save(html_file)
webbrowser.get("firefox").open_new_tab(f"file://{html_file}")
