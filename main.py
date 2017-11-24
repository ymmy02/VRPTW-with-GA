import sys
import subprocess

import ut
from timer import Timer
from solomon import loaddata
from vrptw import VRPTW
from vistools import plot_graphs, draw_routings

def main(filename, output_path="", suffix=None, population=100, \
        generation_span=100, selection="pareto", crossover="bcrc", \
        mutation="inversion", w_nvehicle=100, w_distance=0.001, \
        tournament_size=3, cx_rate=0.6, mu_rate=0.2, mu_irate=0.03):

    Timer.init()
    Timer.start('main')

    path= ut.get_path_from_inputfilename(filename, rslt_dir="results")
    vehicle_capacity_filename = path + "/vehicle_capacity.txt"
    node_filename = filename

    nodes = loaddata(vehicle_capacity_filename, node_filename)
    Timer.check('main', 'load data')

    vrptw = VRPTW()
    vrptw.gaoptimize(nodes, population=population, generation_span=generation_span, \
           selection=selection, crossover=crossover, mutation=mutation, \
           w_nvehicle=w_distance, w_distance=w_distance, tournament_size=tournament_size, \
           cx_rate=cx_rate, mu_rate=mu_rate, mu_irate=mu_irate)
    Timer.check('main', 'optimization')

    best_indv_list = vrptw.get_best_solutions()
    (generations, nvehicle_avgs, distance_avgs, \
            nvehicle_bests, distance_bests) = vrptw.get_records()
    Timer.check('main', 'get result')

    plot_graphs(generations, nvehicle_avgs, distance_avgs, \
            nvehicle_bests, distance_bests, output_path, suffix)
    Timer.check('main', 'plot graphs')

    draw_routings(nodes, best_indv_list, output_path, suffix)
    Timer.check('main', 'draw routings')

    ut.write_results(generations, nvehicle_avgs, distance_avgs, \
            nvehicle_bests, distance_bests, output_path, suffix)
    ut.write_best_solutions(best_indv_list, output_path, suffix)
    Timer.check('main', 'output data')
    Timer.end('main')
    Timer.write(output_path, suffix)


if __name__ == "__main__":
    filename = "dataset/R1/R101.txt"

    # Command Line Arguments
    args = sys.argv
    if len(args) > 1:
        filename = args[1]
        output_path = args[2]
        pop = int(args[3])
        gspan = int(args[4])
        selc = args[5]
        cx = args[6]
        mu = args[7]
        w_nv = float(args[8])
        w_di = float(args[9])
        tournament = int(args[10])
        cx_rate = float(args[11])
        mu_rate = float(args[12])
        mu_irate = float(args[13])
        suffix=1
    main(filename, output_path=output_path, suffix=suffix, population=pop, \
            generation_span=gspan, selection=selc, crossover=cx, mutation=mu, \
            w_nvehicle=w_nv, w_distance=w_di, tournament_size=tournament, \
            cx_rate=cx_rate, mu_rate=mu_rate, mu_irate=mu_irate)
