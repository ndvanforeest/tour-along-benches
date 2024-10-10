import numpy as np

import handle_benches
import handle_graph

from scenario import Scenario


def write_tsplib(project: Scenario):
    "Write distance matrix to file in tsplib format"
    benches = handle_benches.get_benches(project)
    g = handle_graph.get_graph(project)

    distance_matrix = np.array(g.distances(benches, benches), dtype=int)

    with open(project.tsplib_file, "w") as fp:
        fp.write(f"NAME: {project.name}\n")
        fp.write("TYPE: TSP\n")
        fp.write(f"DIMENSION: {len(benches)}\n")
        fp.write("EDGE_WEIGHT_TYPE: EXPLICIT\n")
        fp.write("EDGE_WEIGHT_FORMAT: FULL_MATRIX\n")
        fp.write("DISPLAY_DATA_TYPE: NO_DISPLAY\n")
        for i, s in enumerate(benches):
            fp.write(f"COMMENT: {i}: {s}\n")
        fp.write("EDGE_WEIGHT_SECTION\n")
        fp.write("\n".join(" ".join(map(str, row)) for row in distance_matrix))
        fp.write("\n")
        fp.write("EOF\n")
