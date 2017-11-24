import sys
import subprocess

import ut
from timer import Timer
from solomon import loaddata
from vrptw import VRPTW
from vistools import plot_graphs, draw_routings

def main(filename):
    Timer.init()
    Timer.start('main')

    (path, output_path) = ut.get_paths_from_inputfilename(filename, rslt_dir="results")
    subprocess.call(["mkdir", "-p", output_path])
    vehicle_capacity_filename = path + "/vehicle_capacity.txt"
    node_filename = filename

    nodes = loaddata(vehicle_capacity_filename, node_filename)
    Timer.check('main', 'load data')

    vrptw = VRPTW()
    vrptw.gaoptimize(self, nodes, population=100, generation_span=100, \
           selection="pareto", crossover="bcrc", mutation="inversion", \
           w_nvehicle=100, w_distance=0.01, tournament_size=3, \
           cx_rate=0.6, mu_rate=0.2, mu_irate=0.03)
    Timer.check('main', 'optimization')

    best_indv_list = vrptw.get_best_solutions()
    (generations, nvehicle_avgs, distance_avgs, \
            nvehicle_bests, distance_bests) = vrptw.get_records()
    Timer.check('main', 'get result')

    plot_graphs(generations, nvehicle_avgs, distance_avgs, \
            nvehicle_bests, distance_bests, output_path)
    Timer.check('main', 'plot graphs')

    draw_routings(nodes, best_indv_list, output_path)
    Timer.check('main', 'draw routings')

    Timer.end('main')
    Timer.write(output_path)


if __name__ == "__main__":
    filename = "dataset/R1/R101.txt"

    # Command Line Arguments
    args = sys.argv
    if len(args) > 1:
        filename = args[1]
    main(filename)
