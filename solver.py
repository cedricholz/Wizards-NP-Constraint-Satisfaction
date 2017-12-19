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
    With a 55%, 45% chance, a random wizard or
    the most constrained wizard is chosen, respectively.
    That wizard is then placed in a position that violates
    the least amount of constraints. If the violations
    have not improved in at least 100 iterations, the chosen
    wizard is placed into a random location. If it has
    not improved in 500 iterations, the ordering is shuffled
    and it begins again.

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

        if starting_violations == violations:
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

        if time.time() - start_time > 20:
            break

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

    assigned_string = 'submission_4683299_input20.in,submission_4654473_inputs_input20.in,submission_4712312_inputs_input20.in,submission_4717234_inputs_input35.in,submission_4712495_input35.in,submission_4644349_input50.in,submission_4612341_inputs_input35.in,submission_4716792_input35.in,submission_4717273_input20.in,submission_4715978_input20.in,submission_4710007_input35.in,submission_4718708_input35.in,submission_4697862_input35.in,submission_4702665_inputs_input50.in,submission_4718439_input20.in,submission_4718738_inputs_input50.in,submission_4709529_input20.in,submission_4714521_input35.in,submission_4716635_inputs_input50.in,submission_4715167_inputs_input20.in,submission_4714355_inputs_input35.in,submission_4718430_input20.in,submission_4718752_inputs_input35.in,submission_4717736_input20.in,submission_4714920_input20.in,submission_4700429_inputs_input20.in,submission_4714249_inputs_input20.in,submission_4717053_inputs_input20.in,submission_4716458_input20.in,submission_4714629_inputs_input35.in,submission_4715335_inputs_input35.in,submission_4692735_inputs_input50.in,submission_4698173_input20.in,submission_4718629_input20.in,submission_4716307_inputs_input20.in,submission_4698322_inputs_input50.in,submission_4718782_inputs_input35.in,submission_4718708_input50.in,submission_4718636_inputs_input20.in,submission_4702737_input35.in,submission_4714765_inputs_input50.in,submission_4683124_inputs_input20.in,submission_4699902_input20.in,submission_4718666_input50.in,submission_4718446_inputs_input35.in,submission_4718204_inputs_input20.in,submission_4699284_input20.in,submission_4699902_input35.in'

    assigned_set = set()
    for filename in assigned_string.split(','):
        filename = filename[:filename.index(".")]
        assigned_set.add(filename)


    for file in os.listdir(output_directory):
        filename = os.fsdecode(file)
        filename = filename[:filename.index(".")]
        output_files.add(filename)

    input_files = []

    for file in os.listdir(input_directory):
        filename = os.fsdecode(file)

        filename = filename[:filename.index(".")]

        if filename not in output_files and filename in assigned_set:
            input_files.append(filename)

    for filename in input_files:
        input_file = 'all_submissions/inputs/' + filename + '.in'
        output_file = 'all_submissions/outputs/' + filename + '.out'
        best_so_far_file = 'all_submissions/best_so_far_files/' + filename + '.out'
        multi_process(input_file, output_file, best_so_far_file)


if __name__ == "__main__":
    # phase_2()
    # to_do_list = [140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400]
    # staff_inputs_all_cores_each_input(to_do_list)
    # staff_inputs_one_per_core(to_do_list)
    student_inputs()
