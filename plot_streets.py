#!/usr/bin/env python

import webbrowser

import folium

import handle_streets
from node import find_center
from run_scenario import project

html_file = f"/home/nicky/tmp/html_files/{project.name}_streets.html"

streets = handle_streets.get_streets(project)

center = find_center([n for street in streets for n in street])

m = folium.Map(location=center.gps, zoom_start=16)
for i, street in enumerate(streets):
    path = [n.gps for n in street]
    folium.PolyLine(path, color="blue", weight=1.5, opacity=1).add_to(m)
m.save(html_file)
webbrowser.get("firefox").open_new_tab(f"file://{html_file}")
