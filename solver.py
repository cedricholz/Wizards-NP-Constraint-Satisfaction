import random
import utils
import datetime
import time
import multiprocessing
import sys

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
def place_in_best_location(violations, wizard, wizards, constraint_map):
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
def check_best_violations(violations, wizards, best_so_far_file):
    try:
        with open(best_so_far_file) as f:
            best_violations = int(f.readline().split()[0])
            if violations < best_violations:
                best_list = [str(violations)] + wizards
                utils.write_output(best_so_far_file, best_list)
    except:
        best_list = [str(violations)] + wizards
        utils.write_output(best_so_far_file, best_list)

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
def solve(wizards, constraints, event, best_so_far_file):
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
            # print("Sequence: " + str(sequence))
            # print("Stuck at " + str(violations) + " violations")
            # print(wizards)
            violations = utils.check_violations(wizards, constraint_map)
            sequence = [violations]
    event.set()
    print("\nSolution Sequence" + str(sequence))
    return wizards


"""
Takes the number of wizards and file number
and creates names of the input, output, and
best_so_far files. Runs solver on the inputs,
and writes solution to file.

Input:
    number: number of wizards, 20, 35, or 50
    i: file number 0 - 9
    event: Multithreading event, when one core finds
           A solution and event.set() is called, they
           all stop and move on to the next input
"""
def run_phase2_inputs(number, i, event):
    input_file = 'phase2_inputs/inputs' + number + '/input' + number + '_' + str(i) + '.in'
    output_file = 'phase2_inputs/inputs' + number + '/output' + number + '_' + str(i) + '.out'
    best_so_far_file = 'phase2_inputs/inputs' + number + '/input' + number + '_' + str(i) + '_best_so_far' + '.in'

    print("\nBeginning " + 'input' + number + '_' + str(i))
    num_wizards, num_constraints, wizards, constraints = utils.read_input(input_file)
    solution = solve(wizards, constraints, event, best_so_far_file)
    print("\nFound Solution")
    print(solution)
    utils.write_output(output_file, solution)


"""
Sends an input file task to every cpu
available. Terminates when any of them
finish.

Input:
    number: number of wizards, 20, 35, or 50
    i: file number 0 - 9
"""
def multi_process(number, i):
    cpus_to_use = multiprocessing.cpu_count()

    p = multiprocessing.Pool(cpus_to_use)
    m = multiprocessing.Manager()
    event = m.Event()

    for _ in range(cpus_to_use):
        p.apply_async(run_phase2_inputs, (number, i, event))
    p.close()

    event.wait()
    p.terminate()


"""
Runs the program on the input files.
e.g. multi_process("20", 0) runs on input20_0.in
"""
if __name__ == "__main__":

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

    for i in to_do_list_20:
        multi_process("20", i)

    for i in to_do_list_35:
        multi_process("35", i)

    for i in to_do_list_50:
        multi_process("50", i)
