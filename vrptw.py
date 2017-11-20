import sys, os

import ut
from timer import Timer
from logger import print_log
from gatools import functions as fnc
from gatools import selection, crossover, mutation

class VRPTW(object):
    
    def __init__(self):
        self.is_optimized = False
        self.best_solutions = None
        self.generations = []
        self.nvehicle_avgs = []
        self.distance_avgs = []
        self.nvehicle_bests = []
        self.distance_bests = []

    def gaoptimize(self, nodes, population=100, generation_span=100, \
           selection="parato", crossover="bcrc", mutation="inversion", \
           w_nvehicle=100, w_distance=0.01, tournament_size=3, \
           cx_rate=0.6, mu_rate=0.2, mu_irate=0.03):

        Timer.start("optimize")
        self.generations = []
        self.nvehicle_avgs = []
        self.distance_avgs = []
        self.nvehicle_bests = []
        self.distance_bests = []
        ##############
        # Initialize #
        ##############
        parents = fnc.create_individual_list(population, nodes)
        offsprings = []
        fnc.set_distance(nodes, parents)
        # Evaluate Fitness
        if selection == "wsum":
            for indv in parents:
                indv.fitness = fnc.wsum_evaluate(indv.get_nvehicle(), \
                        indv.distance, w_nvehicle, w_distance)
        elif switch == "ranksum":
            distance_list = [for indv.distance in parents]
            nvehicle_list = [for indv.get_nvehicle() in parents]
            distance_list = list(set(distance_list))
            nvehicle_list = list(set(nvehicle_list))
            for indv in indv_list:
                indv.fitness = distance_list.index(indv.distance)+1 \
                        nvehicle_list.index(indv.get_nvehicle())+1
        self._record(selection, 0, parents)
        Timer.check("optimize", "initalize")


        #############
        # Main Loop #
        #############
        loopcount = 0
        while loopcount < generation_span:
            # Selection
            offsprings = selection.done(selection, parents)
            # Crossover
            offsprings = crossover.done(crossover, nodes, offsprings, rate=cx_rate)
            # Mutation
            offsprings = mutation.done(mutation, nodes, offsprings, \
                    rate=mu_rate, irate=mu_irate)
            # Change Generation
            parents = offsprings[:]
            # Calc Distance
            fnc.set_distance(nodes, parents)
            # Evaluate Fitness
            if selection == "wsum":
                for indv in parents:
                    indv.fitness = fnc.wsum_evaluate(indv.get_nvehicle(), \
                            indv.distance, w_nvehicle, w_distance)
            elif switch == "ranksum":
                distance_list = [for indv.distance in parents]
                nvehicle_list = [for indv.get_nvehicle() in parents]
                distance_list = list(set(distance_list))
                nvehicle_list = list(set(nvehicle_list))
                for indv in indv_list:
                    indv.fitness = distance_list.index(indv.distance)+1 \
                            nvehicle_list.index(indv.get_nvehicle())+1
            # Pick Up Best Solutions
            self.best_solutions = ut.pick_up_best_indvs(selection, parents)
            # Print Log
            loopcount += 1
            self._record(selection, loopcount, parents)
            self._print_log(loopcount)

        Timer.check("optimize", "main loop")

        self.is_optimized = True
        Timer.end("optimize")
        return generations, nvehicle_avgs, distance_avgs, nvehicle_bests, distance_bests

    def get_best_solutions(self):
        if not self.is_optimized:
            print("!!!!! [GA/get_best_indv_list] \
                    Don't call this method before optimize !!!!!")
            sys.exit()
        return self.best_solutions

    def get_records(self):
        if not self.is_optimized:
            print("!!!!! [GA/get_records] \
                    Don't call this method before optimize !!!!!")
            sys.exit()
        return self.generations, self.nvehicle_avgs, \
                self.distance_avgs, self.nvehicle_bests, \
                self.distance_bests

    def _record(self, switch, generation, indv_list):
        best_indv_list = ut.pick_up_best_indvs(switch, indv_list)

        nvehicle_avg = ut.calc_nvehicle_average(indv_list)
        distance_avg = ut.calc_distance_average(indv_list)
        nvehicle_best = ut.calc_nvehicle_average(best_indv_list)
        distance_best = ut.calc_distance_average(best_indv_list)

        self.generations.append(generation)
        self.nvehicle_avgs.append(nvehicle_avg)
        self.distance_avgs.append(distance_avg)
        self.nvehicle_bests.append(nvehicle_best)
        self.distance_bests.append(distance_best)

    def _print_log(generation):
        print("### Best Solutions of Generation", generation, "###")
        for best_indv in self.best_solutions:
            vehicles = best_indv.get_nvehicle()
            distance = best_indv.distance
            print("Vehicles :", vehicles, "Distance :", distance)
