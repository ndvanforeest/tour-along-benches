from functions import run_process
from node import Node


def extract_bounding_box(project):
    south_west = Node(
        0, project.center.lat - project.eps, project.center.lon - project.eps
    )
    north_east = Node(
        0, project.center.lat + project.eps, project.center.lon + project.eps
    )
    command = [
        "osmium",
        "extract",
        "-b",
        f"{south_west.lon},{south_west.lat},{north_east.lon},{north_east.lat}",
        project.source_pbf,
        "-o",
        project.area_pbf,
        "--overwrite",
    ]
    run_process(command)


def extract_relation(project):
    relation_file = f"/home/nicky/tmp/data/{project.name}_relation.pbf"
    command = [
        "osmium",
        "getid",
        "-r",
        "-t",
        project.source_pbf,
        f"r{project.relation}",
        "-o",
        relation_file,
        "--overwrite",
    ]
    run_process(command)
    command = [
        "osmium",
        "extract",
        "-p",
        relation_file,
        project.source_pbf,
        "-o",
        project.area_pbf,
        "--overwrite",
    ]
    run_process(command)


def extract_tags(input_file, output_file, tag_filter):
    command = [
        "osmium",
        "tags-filter",
        input_file,
        *tag_filter,
        "-o",
        output_file,
        "--overwrite",
    ]
    # print(" ".join(command))
    run_process(command)
