#!/usr/bin/env python
import webbrowser

import folium

import handle_benches
import run_scenario

# from statistics import mean
from node import find_center

benches = handle_benches.get_benches(run_scenario.project)

html_file = f"/home/nicky/tmp/html_files/{run_scenario.project.name}_benches.html"

center = find_center(benches)

m = folium.Map(location=center.gps, zoom_start=16)
for bench in benches:
    tooltip = folium.Tooltip(
        f'<div style="white-space: nowrap;"><h2>{bench.name}</h2></div>'
    )
    folium.CircleMarker(
        location=bench.gps,
        popup=bench.name,
        tooltip=tooltip,
        radius=5,
        color="red",
    ).add_to(m)
m.save(html_file)
webbrowser.get("firefox").open_new_tab(f"file://{html_file}")
