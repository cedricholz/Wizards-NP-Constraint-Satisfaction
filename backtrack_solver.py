import random
import utils
import datetime
import time
import multiprocessing
from multiprocessing import Pool
import sys


def check_violates(ordered_wizards, constraint_map):
    prev_wizards = set(ordered_wizards[:1])
    next_wizards = set(ordered_wizards[1:])

    for i in range(1, len(ordered_wizards) - 1):
        cur_wizard = ordered_wizards[i]
        next_wizards.remove(cur_wizard)

        if cur_wizard in constraint_map:
            cur_constraints = constraint_map[cur_wizard]
            for constraint in cur_constraints:
                wizard1 = constraint[0]
                wizard2 = constraint[1]

                if wizard1 in prev_wizards and wizard2 in next_wizards:
                    return True

                elif wizard2 in prev_wizards and wizard1 in next_wizards:
                    return True

        prev_wizards.add(cur_wizard)
    return False


def backtrack_solve(wizards, constraints):
    constraint_map = utils.get_constraint_map(constraints)

    map_copy = dict(constraint_map)
    wizards = utils.sort_wizards(wizards, map_copy)

    def helper(cur_list, wizards_left):
        if len(wizards_left) == 0:
            return cur_list

        for wizard in wizards_left:
            temp_list = cur_list + [wizard]
            violates = check_violates(temp_list, constraint_map)
            if not violates:
                # print(temp_list)
                temp_wizards = wizards_left[:]
                temp_wizards.remove(wizard)
                tested_list = helper(temp_list, temp_wizards)
                if len(tested_list) != 0:
                    return tested_list
        return []

    l = helper([], wizards)
    return l


def run_inputs(event, input_file, output_file, best_so_far_file):
    print("\nBeginning " + input_file)
    num_wizards, num_constraints, wizards, constraints = utils.read_input(input_file)
    solution = backtrack_solve(wizards, constraints)
    print("\nFound Solution")
    print(solution)
    utils.write_output(output_file, solution)


def run_backtrack_inputs(n):
    input_file = n[0] + '.in'
    output_file = n[0] + '.out'
    best_so_far_file = n[0] + '_best_so_far' + '.in'

    run_inputs(n[1], input_file, output_file, best_so_far_file)
    return ("Finished")


def backtrack():
    to_do_list = ['phase2_inputs/inputs20/input20_3', 'phase2_inputs/inputs50/input50_0', 'phase2_inputs/inputs50/input50_8', 'phase2_inputs/inputs50/input50_9']

    m = multiprocessing.Manager()
    event = m.Event()
    inputs = [(x, event) for x in to_do_list]

    number_processes = multiprocessing.cpu_count()

    with Pool(number_processes) as p:
        reslist = [p.apply_async(run_backtrack_inputs, (n,)) for n in inputs]
        for result in reslist:
            print(result.get())


if __name__ == "__main__":
    # phase_2()
    # staff_inputs_all_cores_each_input()
    # staff_inputs_one_per_core()
    backtrack()
