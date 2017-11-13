import sys
import random

from gatools.functions import make_pareto_ranking_list

###########
# Private #
###########
#===!!! Must Have Fitness !!!===#
def _tournament(parents, tournament_size):
    offsprings = []
    for _ in range(len(parents)):
        minfitness = 1e14
        samples = random.sample(parents, tournament_size)
        for salesman in samples:
            if salesman.fitness < minfitness:
                tmp = salesman
                minfitness = salesman.fitness
        offsprings.append(tmp)
    return offsprings 


def _ranksum(parents, tournament_size):
    distance_list = [for indv.distance in parents]
    nvehicle_list = [for indv.get_nvehicle() in parents]

    distance_list = list(set(distance_list))
    nvehicle_list = list(set(nvehicle_list))

    for indv in parents:
        indv.fitness = distance_list.index(indv.distance)+1 \
                nvehicle_list.index(indv.get_nvehicle())+1

    return _tournament(parents, tournament_size)


def _pareto_ranking(parents):
    indv_list = parents
    ranking_list = []
    offsprings = []

    ranking_list = make_pareto_ranking_list(indv_list)

    size = len(ranking_list)
    npart = int((size*(size+1)) / 2)
    part = 1.0 / npart

    uniform = random.random()

    span = 0.0
    for _ in range(len(parents)):
        for i in range(size):
            span += (size-i) * part
            if uniform < span:
                choice = random.choice(ranking_list[i])
                offsprings.append(choice)
                break
    
    return offsprings

##########
# Public #
##########
def done(switch, parents, tournament_size=3):
    if switch == "pareto":
        offsprings =  _pareto_ranking(parents)
    elif switch == "wsum":
        offsprings =  _tournament(parents, tournament_size)
    elif switch == "ranksum":
        offsprings = _ranksum(parents, tournament_size)
    else:
        print("!!!!! [selection/done] switch doesn't has such paramerter !!!!!")
        sys.exit()

    return offsprings
