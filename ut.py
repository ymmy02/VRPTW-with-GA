from gatools import functions as fnc

def flatten(chromosome):
    return [node for route in chromosome for node in route]


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
    if selection == "pareto":
        (best_solutions, others) = fnc.make_current_ranking_list(indv_list)
        others = []
    elif switch in ["wsum", "ranksum"]
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
