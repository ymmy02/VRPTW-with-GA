import sys,os
sys.path.append(os.pardir)
import ut
import random
import copy

from timer import Timer
import gatools.functions as fnc

###########
# Private #
###########
#=====<Insersion>=====#
def _random_choice_and_reinsert(chromosome, nodes):
    i = random.choice(range(len(chromosome)))
    j = random.choice(range(len(chromosome[i])))
    insert_node = chromosome[i].pop(j)
    feasible_list = []
    for (i, route) in enumerate(chromosome):
        if nodes.is_feasible(route+[insert_node]):
            feasible_list.append(i)
    if len(feasible_list) == 0:   # Is Empty
        chromosome.append([insert_node])
    else:
        i = random.choice(feasible_list)
        j = random.choice(range(len(chromosome[i])+1))
    chromosome[i].insert(j, insert_node)

def _insertion(nodes, chromosome, rate=0.02):
    size = len(ut.flatten(chromosome))
    for _ in range(size):
        if random.random() < rate:
            _random_choice_and_reinsert(chromosome, nodes)
    return chromosome
#=====</Insersion>=====#

#=====<Inversion>=====#
def _inversion(nodes, chromosome):
    flat_route = ut.flatten(chromosome)
    size = len(flat_route)
    cut1 = random.randint(0, size-1)
    cut2 = random.randint(cut1+1, size)
    reverse_part = flat_route[cut1:cut2]
    reverse_part.reverse()
    new_flat_route = flat_route[0:cut1] + reverse_part \
            + flat_route[cut2:size]
    new_chromosome = fnc.shape_flat_to_vehicles(nodes, new_flat_route)
    return new_chromosome
#=====</Inversion>=====#


##########
# Public #
##########
def done(switch, nodes, offsprings, rate=0.3, irate=0.02):
    Timer.start("mutation")
    new_offsprings = []
    for indv in offsprings:
        tmp = copy.deepcopy(indv)
        if random.random() < rate:
            if switch == "insersion":
                tmp.chromosome = _insertion(nodes, indv.chromosome)
            elif switch == "inversion":
                tmp.chromosome = _inversion(nodes, indv.chromosome)
            else:
                print("!!!!! [mutation/done] switch doesn't has such paramerter:", \
                        switch, "!!!!!")
                sys.exit()
        tmp.chromosome = fnc.remove_null_route(tmp.chromosome)    # Remove the route which has no nodes
        new_offsprings.append(tmp)
    Timer.end("mutation")
    return new_offsprings
