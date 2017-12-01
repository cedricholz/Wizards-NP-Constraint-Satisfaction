import random
import utils
import datetime
import time
import multiprocessing
from multiprocessing import Pool
import sys
import os
import math


def place_in_best_location(violations, wizard, w, constraint_map):
    """
    Places a wizard in the location causing
    the least amount of constraint violations

    Input:
        violations: Number of constraint violations to beat
        wizard: Wizard we're finding a better place for
        wizards: Current ordering of the wizards
        constraint_map: Wizard names mapped to a list of their constraits

    Output:
        best_cur_violations: Number of violations after the move
    """
    wizards = w[:]

    best_cur_violations = violations
    best_j = wizards.index(wizard)
    wizards.remove(wizard)
    wizards = [wizard] + wizards

    for j in range(len(wizards) - 1):
        temp_violations = utils.check_total_violations(wizards, constraint_map)
        if temp_violations <= best_cur_violations:
            best_cur_violations = temp_violations
            best_j = j
        wizards[j], wizards[j + 1] = wizards[j + 1], wizards[j]
    wizards.pop()
    wizards.insert(best_j, wizard)
    return best_cur_violations, wizards


def place_in_random_location(wizard, wizards, constraint_map):
    random_i = random.randrange(0, len(wizards) - 1)
    random_j = random.randrange(0, len(wizards) - 1)

    wizards[random_i], wizards[random_j] = wizards[random_j], wizards[random_i]
    violations = utils.check_total_violations(wizards, constraint_map)

    return violations, wizards

def solve(wizards, constraints, event, best_so_far_file):
    """
    Takes an ordering of wizards, and one by one
    (most constrained first) places them in the location
    that causes the least amount of constraint violations.
    If it gets stuck at a place where no single move
    decreases the amount of violations, it shuffles
    the ordering and starts again.

    Input:
        wizards: Number of constraint violations to beat
        constraints: Constraints from inputfile
        event: Multithreading event, when one core finds
               A solution and event.set() is called, they
               all stop and move on to the next input
        best_so_far_file: name of the file containing the
                          best ordering found so far
    Output:
        wizards: A valid ordering of the wizards
    """
    constraint_ordering = wizards[:]
    constraint_map = utils.get_constraint_map(constraints)

    violations = utils.check_total_violations(wizards, constraint_map)

    best_found = sys.maxsize
    count = 0


    start_time = time.time()
    while violations > 0:

        starting_violations = violations

        # Choose a random wizard or the most constrained wizard
        random_or_most_constrained_val = random.randrange(0, 100)
        if random_or_most_constrained_val < 55:
            wizard = random.choice(constraint_ordering)
        else:
            constraint_ordering = utils.sort_wizards(wizards, constraint_map)
            wizard = constraint_ordering[0]

        violations, wizards = place_in_best_location(violations, wizard, wizards, constraint_map)

        if starting_violations == violations and violations:
            count += 1
            if count >= 500:
                count = 0
                random.shuffle(wizards)
                violations = utils.check_total_violations(wizards, constraint_map)

                # print("Stuck at " + str(violations) + " violations")
                # print(wizards)
            elif count >= 100:
                wizard = random.choice(constraint_ordering)
                violations, wizards = place_in_random_location(wizard, wizards, constraint_map)
        else:
            utils.check_best_violations(violations, wizards, best_so_far_file)
            count = 0
        if time.time() - start_time > 180:
            event.set()

    event.set()
    return wizards



def run_inputs(event, input_file, output_file, best_so_far_file):
    print("\nBeginning " + input_file)
    num_wizards, num_constraints, wizards, constraints = utils.read_input(input_file)
    solution = solve(wizards, constraints, event, best_so_far_file)
    print("\nFound Solution")
    print(solution)
    utils.write_output(output_file, solution)


def multi_process(input_file, output_file, best_so_far_file):

    cpus_to_use = multiprocessing.cpu_count()


    p = multiprocessing.Pool(cpus_to_use)
    m = multiprocessing.Manager()
    event = m.Event()

    for _ in range(cpus_to_use):
        p.apply_async(run_inputs, (event, input_file, output_file, best_so_far_file))
    p.close()

    event.wait()
    p.terminate()


def get_phase_2_file_names(num_wizards, file_num):
    input_file = 'phase2_inputs/inputs' + num_wizards + '/input' + num_wizards + '_' + file_num + '.in'
    output_file = 'phase2_inputs/inputs' + num_wizards + '/output' + num_wizards + '_' + file_num + '.out'
    best_so_far_file = 'phase2_inputs/inputs' + num_wizards + '/input' + num_wizards + '_' + file_num + '_best_so_far' + '.in'
    return input_file, output_file, best_so_far_file


def phase_2():
    """
    Runs the program on the phase_2 input files.
    e.g. multi_process("20", 0) runs on input20_0.in
    """

    # Full list of inputs

    # Solvable
    to_do_list_20 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    to_do_list_35 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    to_do_list_50 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    for file_num in to_do_list_20:
        input_file, output_file, best_so_far_file = get_phase_2_file_names("20", str(file_num))
        multi_process(input_file, output_file, best_so_far_file)

    for file_num in to_do_list_35:
        input_file, output_file, best_so_far_file = get_phase_2_file_names("35", str(file_num))
        multi_process(input_file, output_file, best_so_far_file)

    for file_num in to_do_list_50:
        input_file, output_file, best_so_far_file = get_phase_2_file_names("50", str(file_num))
        multi_process(input_file, output_file, best_so_far_file)


def staff_inputs_all_cores_each_input(to_do_list):

    for n in to_do_list:
        input_file = 'Staff_Inputs/staff_' + str(n) + '.in'
        output_file = 'Staff_Inputs/staff_' + str(n) + '.out'
        best_so_far_file = 'Staff_Inputs/staff_' + str(n) + '_best_so_far' + '.in'
        multi_process(input_file, output_file, best_so_far_file)


def run_staff_inputs_one_per_core(n):
    input_file = 'Staff_Inputs/staff_' + str(n[0]) + '.in'
    output_file = 'Staff_Inputs/staff_' + str(n[0]) + '.out'
    best_so_far_file = 'Staff_Inputs/staff_' + str(n[0]) + '_best_so_far' + '.in'

    run_inputs(n[1], input_file, output_file, best_so_far_file)
    return ("Finished")


def staff_inputs_one_per_core(to_do_list):
    m = multiprocessing.Manager()
    event = m.Event()
    inputs = [(x, event) for x in to_do_list]

    number_processes = multiprocessing.cpu_count()

    with Pool(number_processes) as p:
        reslist = [p.apply_async(run_staff_inputs_one_per_core, (n,)) for n in inputs]
        for result in reslist:
            print(result.get())


def student_inputs():
    input_directory = os.fsencode("all_submissions/inputs")

    output_directory = os.fsencode("all_submissions/outputs")

    output_files = set()

    for file in os.listdir(output_directory):
        filename = os.fsdecode(file)
        filename = filename[:filename.index(".")]
        output_files.add(filename)

    input_files = []
    for file in os.listdir(input_directory):
        filename = os.fsdecode(file)

        filename = filename[:filename.index(".")]

        if filename not in output_files:
            input_files.append(filename)

    for filename in input_files:
        input_file = 'all_submissions/inputs/' + filename + '.in'
        output_file = 'all_submissions/outputs/' + filename + '.out'
        best_so_far_file = 'all_submissions/best_so_far_files/' + filename + '.out'
        multi_process(input_file, output_file, best_so_far_file)


if __name__ == "__main__":

    phase_2()
    to_do_list = [140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400]
    # staff_inputs_all_cores_each_input(to_do_list)
    # staff_inputs_one_per_core(to_do_list)
    # student_inputs()
