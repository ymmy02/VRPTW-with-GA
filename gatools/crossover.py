import sys,os
sys.path.append(os.pardir)
import ut
import random
import copy
import time

from timer import Timer
import gatools.functions as fnc

###########
# Private #
###########
def _insert_node(nodes, new_chromosome, L):
    for insert_node in L:
        feasible_list = []
        for (i, route) in enumerate(new_chromosome):
            for j in range(len(route)+1):
                tmp = route[0:j] + [insert_node] + route[j:]
                if nodes.is_feasible(tmp):
                    feasible_list.append((i, j))
        if len(feasible_list) == 0:   # Is Empty
            new_chromosome.append([insert_node])
        else:
            (i, j) = random.choice(feasible_list)
            new_chromosome[i].insert(j, insert_node)

#===<Route Crossover>===#
def _route_crossover(nodes, offsprings, rate=0.5):
    new_offsprings = []
    half = int(len(offsprings)/2)

    for (indv1, indv2) in zip (offsprings[0:half], offsprings[half:]):
        tmp1 = copy.deepcopy(indv1)
        tmp2 = copy.deepcopy(indv2)
        if random.random() < rate:
            (tmp1.chromosome, tmp2.chromosome) =        \
                  _rc(nodes, indv1.chromosome, indv2.chromosome)
        tmp1.chromosome = fnc.remove_null_route(tmp1.chromosome)   # Remove the route which has no nodes
        tmp2.chromosome = fnc.remove_null_route(tmp2.chromosome)
        new_offsprings.append(tmp1)
        new_offsprings.append(tmp2)
    return new_offsprings

def _mask(chromosome):
    L = []
    new_chromosome = []
    for route in chromosome:
        if random.random() < 0.5:
            L.extend(route)
        else:
            new_chromosome.append(route)
    return L, new_chromosome

def _rearrange_in_counterpart_order(L, ch_onerow):
    return [i for i in ch_onerow if i in L]
  
def _rc(nodes, ch1, ch2):
    L1, new_ch1 = _mask(ch1)
    L2, new_ch2 = _mask(ch2)
    ch1_onerow = ut.flatten(ch1)
    ch2_onerow = ut.flatten(ch2)
    L1 = _rearrange_in_counterpart_order(L1, ch2_onerow)
    L2 = _rearrange_in_counterpart_order(L2, ch1_onerow)
    _insert_node(nodes, new_ch1, L1)
    _insert_node(nodes, new_ch2, L2)

    return new_ch1, new_ch2
#===</Route Crossover>===#


#===<Best Cost Route Crossover>===#
def _best_cost_route_crossover(nodes, offsprings, rate):
    new_offsprings = []
    half = int(len(offsprings)/2)

    for (indv1, indv2) in zip (offsprings[0:half], offsprings[half:]):
        tmp1 = copy.deepcopy(indv1)
        tmp2 = copy.deepcopy(indv2)
        if random.random() < rate:
            (tmp1.chromosome, tmp2.chromosome) =        \
                  _bcrc(nodes, indv1.chromosome, indv2.chromosome)
        tmp1.chromosome = fnc.remove_null_route(tmp1.chromosome)   # Remove the route which has no nodes
        tmp2.chromosome = fnc.remove_null_route(tmp2.chromosome)
        new_offsprings.append(tmp1)
        new_offsprings.append(tmp2)
    return new_offsprings

def _delete_nodes(chromosome, route):
    remove_index_list = []
    chromosome_deleated = []
    for rt in chromosome:
        route_deleated = [node for node in rt if node not in route]
        chromosome_deleated.append(route_deleated)
    return chromosome_deleated

def _bcrc(nodes, ch1, ch2):
    route1 = random.choice(ch1)
    route2 = random.choice(ch2)
    ch1 = _delete_nodes(ch1, route2)
    ch2 = _delete_nodes(ch2, route1)
    _insert_node(nodes, ch1, route2)
    _insert_node(nodes, ch2, route1)
    return ch1, ch2
#===</Best Cost Route Crossover>===#


#===<Uniform Order Crossover(UOX)>===#
def _uox(nodes, ch1, ch2):
    flattench1 = ut.flatten(ch1)
    flattench2 = ut.flatten(ch2)
    size = len(flattench1)
    mask = [random.randint(0, 1) for i in range(size)]

    tmpch1 = [flattench1[i]*mask[i] for i in range(size)]
    tmpch2 = [flattench2[i]*mask[i] for i in range(size)]

    for i in range(size):
        if flattench2[i] not in tmpch1:
            insert_index = tmpch1.index(0)
            tmpch1[insert_index] = flattench2[i]
    for i in range(size):
        if flattench1[i] not in tmpch2:
            insert_index = tmpch2.index(0)
            tmpch1[insert_index] = flattench1[i]

    tmpch1 = fnc.shape_flat_to_vehicles(nodes, tmpch1)
    tmpch2 = fnc.shape_flat_to_vehicles(nodes, tmpch2)

    return tmpch1, tmpch2

def _uniform_order_crossover(nodes, offsprings, rate):
    new_offsprings = []
    half = int(len(offsprings)/2)

    for (indv1, indv2) in zip (offsprings[0:half], offsprings[half:]):
        tmp1 = copy.deepcopy(indv1)
        tmp2 = copy.deepcopy(indv2)
        if random.random() < rate:
            (tmp1.chromosome, tmp2.chromosome) =        \
                  _uox(nodes, indv1.chromosome, indv2.chromosome)
        tmp1.chromosome = fnc.remove_null_route(tmp1.chromosome)   # Remove the route which has no nodes
        tmp2.chromosome = fnc.remove_null_route(tmp2.chromosome)
        new_offsprings.append(tmp1)
        new_offsprings.append(tmp2)
    return new_offsprings
#===</Uniform Order Crossover(UOX)>===#


#===<Partially Mapped Crossover(PMX)>===#
def _get_no_conflict_list(origin, counterpart):
    for i in range(len(origin)):
        if origin[i] in counterpart:
            origin[i] = 0
    return origin

def _pmx(nodes, ch1, ch2):
    flattench1 = ut.flatten(ch1)
    flattench2 = ut.flatten(ch2)
    size = len(flattench1)
    point1 = random.randint(0, size-1)
    point2 = random.randint(point1+1, size)

    tmp = flattench2[point1:point2]
    pre = _get_no_conflict_list(flattench1[0:point1], tmp)
    suf = _get_no_conflict_list(flattench1[point2:], tmp)
    tmpch1 = pre + tmp + suf
    tmp = flattench1[point1:point2]
    pre = _get_no_conflict_list(flattench2[0:point1], tmp)
    suf = _get_no_conflict_list(flattench2[point2:], tmp)
    tmpch2 = pre + tmp + suf

    for node in flattench2:
        if node not in tmpch1:
            insert_index = tmpch1.index(0)
            tmpch1[insert_index] = node
    for node in flattench1:
        if node not in tmpch2:
            insert_index = tmpch2.index(0)
            tmpch2[insert_index] = node

    tmpch1 = fnc.shape_flat_to_vehicles(nodes, tmpch1)
    tmpch2 = fnc.shape_flat_to_vehicles(nodes, tmpch2)
    return tmpch1, tmpch2

def _partially_mapped_crossover(nodes, offsprings, rate):
    new_offsprings = []
    half = int(len(offsprings)/2)

    for (indv1, indv2) in zip (offsprings[0:half], offsprings[half:]):
        tmp1 = copy.deepcopy(indv1)
        tmp2 = copy.deepcopy(indv2)
        if random.random() < rate:
            (tmp1.chromosome, tmp2.chromosome) =        \
                  _pmx(nodes, indv1.chromosome, indv2.chromosome)
        tmp1.chromosome = fnc.remove_null_route(tmp1.chromosome)   # Remove the route which has no nodes
        tmp2.chromosome = fnc.remove_null_route(tmp2.chromosome)
        new_offsprings.append(tmp1)
        new_offsprings.append(tmp2)
    return new_offsprings
#===</Partially Mapped Crossover(PMX)>===#


##########
# Public #
##########
def done(switch, nodes, offsprings, rate=0.6):
    Timer.start("crossover")
    if switch == "uox":
        new_offsprings =  _uniform_order_crossover(nodes, offsprings, rate)
    elif switch == "pmx":
        new_offsprings =  _partially_mapped_crossover(nodes, offsprings, rate)
    elif switch == "rc":
        new_offsprings =  _route_crossover(nodes, offsprings, rate)
    elif switch == "bcrc":
        new_offsprings = _best_cost_route_crossover(nodes, offsprings, rate)
    else:
        print("!!!!! [crossover/done] switch doesn't has such paramerter:", \
                switch, "!!!!!")
        sys.exit()
    Timer.end("crossover")

    return new_offsprings
