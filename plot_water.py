#!/usr/bin/env python
import webbrowser

import folium

import handle_water_areas
from node import find_center
from run_scenario import project

water_areas = handle_water_areas.get_water_areas(project)

html_file = f"/home/nicky/tmp/html_files/{project.name}_water.html"

center = find_center([p for outer_ring, _ in water_areas for p in outer_ring])

m = folium.Map(location=center.gps, zoom_start=15)

water_polygons = handle_water_areas.convert_area_to_polygon(water_areas)
for polygon in water_polygons:
    geo_json = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[(y, x) for x, y in polygon.exterior.coords]]
            + [[(y, x) for x, y in interior.coords] for interior in polygon.interiors],
        },
        "properties": {"name": "Water Area"},
    }
    folium.GeoJson(
        geo_json,
        style_function=lambda x: {
            "fillColor": "blue",
            "color": "blue",
            "weight": 2,
            "fillOpacity": 0.2,
        },
    ).add_to(m)


m.save(html_file)
webbrowser.get("firefox").open_new_tab(f"file://{html_file}")
