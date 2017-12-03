import sys
from gatools import functions as fnc

def flatten(chromosome):
    return [node for route in chromosome for node in route]


def get_path_from_inputfilename(filename, rslt_dir="results"):
    path_list = filename.split('/')
    path = '/'.join(path_list[:-1])
    return path


def remove_duplication(indv_list):
  nodupl_list = [indv_list[0]]
  for indv1 in indv_list[1:]:
    flag_add = True
    for indv2 in nodupl_list:
      if indv1 == indv2:
        flag_add = False
        break
    if flag_add:
      nodupl_list.append(indv1)
  return nodupl_list


def calc_nvehicle_average(indv_list):
    avg = 0
    for indv in indv_list:
        avg += indv.get_nvehicle()
    return avg/len(indv_list)

def calc_distance_average(indv_list):
    avg = 0
    for indv in indv_list:
        avg += indv.distance
    return avg/len(indv_list)

def pick_up_best_indvs(switch, indv_list):
    best_solutions = []
    if switch == "pareto":
        (best_solutions, others) = fnc.make_current_ranking_list(indv_list)
        others = []
    elif switch in ["wsum", "ranksum"]:
        best_indv = indv_list[0]
        for indv in indv_list:
            if indv.fitness < best_indv.fitness:
                best_indv = indv
        best_solutions = [best_indv]
    else:
        print("!!!!! [ut/pick_up_best_indvs] switch doesn't has such paramerter:", \
                switch, "!!!!!")
        sys.exit()

    return remove_duplication(best_solutions)

def add_suffix(filename, suffix=None):
    if suffix is not None:
        suffix = "_" + str(suffix).zfill(3)
        new_filename = filename + suffix
    else:
        new_filename = filename 
    return new_filename

def write_results(generations, nvehicle_avgs, distance_avgs, \
        nvehicle_bests, distance_bests, path="", suffix=None):
    if len(path) != 0:
        path = path + "/"
    filename = add_suffix("output", suffix) + ".dat"

    f = open(path + filename, 'w')
    for i in range(len(generations)):
        ge = str(generations[i]) + " "
        na = str(nvehicle_avgs[i]) + " "
        da = str(distance_avgs[i]) + " "
        nb = str(nvehicle_bests[i]) + " "
        db = str(distance_bests[i]) + "\n"
        f.write(ge + na + da + nb + db)
    f.close()

def write_best_solutions(best_indv_list, path="", suffix=None):
    if len(path) != 0:
        path = path + "/"
    filename = add_suffix("best_solutions", suffix) + ".dat"

    # Number of Vehicles, Total Distance
    f = open(path + filename, 'w')
    for indv in best_indv_list:
        nvihecle = str(indv.get_nvehicle())
        distance = str(indv.distance)
        f.write(nvihecle + " " + distance + "\n")
    f.close()

    # Routings
    for (i, indv) in enumerate(best_indv_list):
        filename = add_suffix("routing" + str(i).zfill(3), suffix) + ".txt"
        f = open(path + filename, 'w')
        for route in indv.chromosome:
            f.write(str(route) + "\n")
        f.close()
