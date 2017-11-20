import random
import utils
import datetime
import time
import multiprocessing
from multiprocessing import Pool
import sys


def place_in_best_location(violations, wizard, wizards, constraint_map):
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
    best_cur_violations = violations

    best_j = wizards.index(wizard)
    wizards.remove(wizard)
    wizards = [wizard] + wizards

    for j in range(len(wizards) - 1):
        temp_violations = utils.check_violations(wizards, constraint_map)
        if temp_violations < best_cur_violations:
            best_cur_violations = temp_violations
            best_j = j
        wizards[j], wizards[j + 1] = wizards[j + 1], wizards[j]
    wizards.pop()
    wizards.insert(best_j, wizard)

    return best_cur_violations, wizards


def check_best_violations(violations, wizards, best_so_far_file):
    """
    Checks the current wizard ordering against a file
    containing the best ordering we've seen so far
    and the number of constraints it violates. Has to
    be in a file because the program is running on
    multiple cores.

    Input:
        violations: Violations the wizard ordering has
        wizards: The wizard ordering
        best_so_far_file: name of the file containing the
                          best ordering found so far
    """
    try:
        with open(best_so_far_file) as f:
            best_violations = int(f.readline().split()[0])
            if violations < best_violations:
                best_list = [str(violations)] + wizards
                print("Best violations updated: " + violations + " " + best_so_far_file)
                utils.write_output(best_so_far_file, best_list)
    except:
        best_list = [str(violations)] + wizards
        utils.write_output(best_so_far_file, best_list)


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
    constraint_map = utils.get_constraint_map(constraints)
    violations = utils.check_violations(wizards, constraint_map)

    sorted_wizards = utils.sort_wizards(wizards, constraint_map)

    sequence = [violations]
    best_found = sys.maxsize
    while violations > 0:

        starting_violations = violations

        for wizard in sorted_wizards:
            violations, wizards = place_in_best_location(violations, wizard, wizards, constraint_map)

            check_best_violations(violations, wizards, best_so_far_file)

            sequence.append(violations)
        if starting_violations == violations:
            random.shuffle(wizards)
            random.shuffle(sorted_wizards)
            print("Sequence: " + str(sequence))
            print("Stuck at " + str(violations) + " violations")
            print(wizards)
            violations = utils.check_violations(wizards, constraint_map)
            sequence = [violations]
    event.set()
    print("\nSolution Sequence" + str(sequence))
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
    # to_do_list_20 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # to_do_list_35 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # to_do_list_50 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Unable to solve
    # to_do_list_20 = [3]
    # to_do_list_35 = []
    # to_do_list_50 = [0, 8, 9]

    # Solvable
    to_do_list_20 = [0, 1, 2, 4, 5, 6, 7, 8, 9]
    to_do_list_35 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    to_do_list_50 = [1, 2, 3, 4, 5, 6, 7]

    for file_num in to_do_list_20:
        input_file, output_file, best_so_far_file = get_phase_2_file_names("20", str(file_num))
        multi_process(input_file, output_file, best_so_far_file)

    for file_num in to_do_list_35:
        input_file, output_file, best_so_far_file = get_phase_2_file_names("35", str(file_num))
        multi_process(input_file, output_file, best_so_far_file)

    for number in to_do_list_50:
        input_file, output_file, best_so_far_file = get_phase_2_file_names("50", str(file_num))
        multi_process(input_file, output_file, best_so_far_file)


def staff_inputs_all_cores_each_input():
    to_do_list = [60, 80, 100, 120, 140, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400]

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


def staff_inputs_one_per_core():
    to_do_list = [60, 80, 100, 120, 140, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400]
    m = multiprocessing.Manager()
    event = m.Event()
    inputs = [(x, event) for x in to_do_list]

    number_processes = multiprocessing.cpu_count()

    with Pool(number_processes) as p:
        reslist = [p.apply_async(run_staff_inputs_one_per_core, (n,)) for n in inputs]
        for result in reslist:
            print(result.get())


if __name__ == "__main__":
    # phase_2()
    # staff_inputs_all_cores_each_input()
    staff_inputs_one_per_core()
