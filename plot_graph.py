#!/usr/bin/env python
import webbrowser
from statistics import mean

import folium

import handle_graph
import run_scenario

graph = handle_graph.get_graph(run_scenario.project)

html_file = f"/home/nicky/tmp/html_files/{run_scenario.project.name}_graph.html"

mean_lat = mean(v.lat for v in graph.vertices())
mean_lon = mean(v.lon for v in graph.vertices())

m = folium.Map(location=(mean_lat, mean_lon), zoom_start=16)
for edge in graph.edges():
    path = [(n.lat, n.lon) for n in edge]
    folium.PolyLine(path, color="blue", weight=2.5, opacity=0.8).add_to(m)


m.save(html_file)
webbrowser.get("firefox").open_new_tab(f"file://{html_file}")
