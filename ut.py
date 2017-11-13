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


def pick_up_best_indvs(indv_list, selection="pareto"):
    best_solutions = []
    if selection == "pareto":
        (best_solutions, others) = fnc.make_current_ranking_list(indv_list)
        others = []
    return remove_duplication(best_solutions)
