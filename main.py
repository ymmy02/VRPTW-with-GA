from timer import Timer
from solomon import loaddata
from vrptw import VRPTW
from visualize import plot_graphs, draw_routings

def main(filename):
    Timer.init()
    Timer.start('main')

    nodes = loaddata(filename)
    Timer.check('main', 'load data')

    vrptw = VRPTW()
    vrptw.gaoptimize(nodes)
    Timer.check('main', 'optimization')

    best_indv_list = vrptw.get_best_indv_list()
    (generations, nvehicle_avgs, distance_avgs, \
            nvehicle_bests, distance_bests) = vrptw.get_records()
    Timer.check('main', 'get result')

    plot_graphs(generations, nvehicle_avgs, distance_avgs, \
            nvehicle_bests, distance_bests)
    Timer.check('main', 'plot graphs')

    draw_routings(best_indv_list)
    Timer.check('main', 'draw routings')

    Timer.end('main')


if __name__ == "__main__":
    # Command Line Arguments
    main(filename)
