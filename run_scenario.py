from pytictoc import TicToc

import compute_tour
import handle_benches
import handle_gates
import handle_graph
import handle_streets
import handle_water_areas
import osmium_extract
import insert_benches_in_graph
import write_tsplib


tt = TicToc()
tt.tic()


# Choose a scenario

# from scenarios import trompbrug as project
# from scenarios import hoornse_pad as project
# from scenarios import graafadolfstraat as project
# from scenarios import groningen_centrum as project
# from scenarios import groningen_city as project
from scenarios import groningen_municipality as project

# from scenarios import adamzuid as project


def do_all():
    "Compute the tsp along the benches in the project."
    if project.relation > 0:
        osmium_extract.extract_relation(project)
    elif project.center.ref != 0:
        osmium_extract.extract_bounding_box(project)
    else:
        print("Project does not have a relation of bounding box")
        quit()
    tt.toc("Osmium files extracted", restart=True)
    handle_benches.make_pkl(project)
    benches = handle_benches.get_benches(project)
    print("Number of benches: ", len(benches))
    handle_streets.make_pkl(project)
    handle_gates.make_pkl(project)
    handle_water_areas.make_pkl(project)
    tt.toc("handlers complete", restart=True)
    handle_graph.make_graph(project)
    tt.toc("graph made", restart=True)
    insert_benches_in_graph.make_pkl(project)
    tt.toc("benches added to graph", restart=True)
    handle_graph.compute_lengths(project)
    tt.toc("edge lengths computed", restart=True)
    write_tsplib.write_tsplib(project)
    tt.toc("tspfile written", restart=True)
    compute_tour.make_tour(project)
    tt.toc("tsp like tour computed", restart=True)


def do_partial():
    "A few computational steps, just for fast testing."
    # handle_graph.make_graph(project)
    # tt.toc("graph made", restart=True)
    insert_benches_in_graph.make_pkl(project)
    tt.toc("benches added to graph", restart=True)
    handle_graph.compute_lengths(project)
    tt.toc("edge lengths computed", restart=True)
    write_tsplib.write_tsplib(project)
    tt.toc("tspfile written", restart=True)
    compute_tour.make_tour(project)
    tt.toc("tsp like tour computed", restart=True)


if __name__ == "__main__":
    do_all()
    # do_partial()
