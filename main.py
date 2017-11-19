from timer import Timer
from solomon import loaddata
from vrptw import VRPTW
from visualize import plot_graphs, draw_routings

def main(filename):
    timer = Timer()
    timer.start('main')

    nodes = loaddata(filename)
    timer.check('main', 'load data')

    vrptw = VRPTW()
    vrptw.gaoptimize(nodes)
    timer.check('main', 'optimization')

    best_indv_list = vrptw.get_best_indv_list()
    (generations, nvehicle_avgs, distance_avgs, \
            nvehicle_bests, distance_bests) = vrptw.get_records()
    timer.check('main', 'get result')

    plot_graphs(generations, nvehicle_avgs, distance_avgs, \
            nvehicle_bests, distance_bests)
    timer.check('main', 'plot graphs')

    draw_routings(best_indv_list)
    timer.check('main', 'draw routings')

    timer.end('main')


if __name__ == "__main__":
    # Command Line Arguments
    main(filename)
