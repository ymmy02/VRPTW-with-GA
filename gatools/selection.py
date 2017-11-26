import sys,os
sys.path.append(os.pardir)

import random

from timer import Timer
from gatools.functions import make_pareto_ranking_list

###########
# Private #
###########
#===!!! Must Have Fitness !!!===#
def _tournament(parents, tournament_size, elite_size=0):
    Timer.start("tournament")
    offsprings = []

    # Elitism
    for _ in range(elite_size):
        minfitness = 1e14
        minindex = -1
        for (i, indv) in enumerate(parents):
            if indv.fitness < minfitness:
                minindex = i
                minfitness = indv.fitness
        tmp = parents.pop(minindex)
        offsprings.append(tmp)
    parents.extend(offsprings)
    Timer.check("tournament", "elitism")

    for _ in range(len(parents)-elite_size):
        minfitness = 1e14
        samples = random.sample(parents, tournament_size)
        for salesman in samples:
            if salesman.fitness < minfitness:
                tmp = salesman
                minfitness = salesman.fitness
        offsprings.append(tmp)
    Timer.check("tournament", "choice")
    Timer.end("tournament")
    return offsprings 


def _ranksum(parents, tournament_size, elite_size=0):
    return _tournament(parents, tournament_size, elite_size)


def _pareto_ranking(parents, elite_size=0):
    Timer.start("pareto")
    indv_list = parents
    ranking_list = []
    offsprings = []

    ranking_list = make_pareto_ranking_list(indv_list)

    size = len(ranking_list)
    npart = int((size*(size+1)) / 2)
    part = 1.0 / npart

    uniform = random.random()
    Timer.check("pareto", "make rank")

    # Elitism
    count = 0
    for rank in ranking_list:
        if count > elite_size:
            break
        for elite in rank:
            offsprings.append(elite)
            count += 1
    Timer.check("pareto", "elitism")

    span = 0.0
    for _ in range(len(parents)-elite_size):
        for i in range(size):
            span += (size-i) * part
            if uniform < span:
                choice = random.choice(ranking_list[i])
                offsprings.append(choice)
                break
    Timer.check("pareto", "choice")
    
    Timer.end("pareto")
    return offsprings

##########
# Public #
##########
def done(switch, parents, tournament_size=3, elite_size=0):
    Timer.start("selection")
    if switch == "pareto":
        offsprings =  _pareto_ranking(parents, elite_size)
    elif switch == "wsum":
        offsprings =  _tournament(parents, tournament_size, elite_size)
    elif switch == "ranksum":
        offsprings = _ranksum(parents, tournament_size, elite_size)
    else:
        print("!!!!! [selection/done] switch doesn't has such paramerter:", \
                switch, "!!!!!")
        sys.exit()
    Timer.end("selection")

    return offsprings
