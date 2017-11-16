import random
import utils
import datetime
import time
import multiprocessing
import sys


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


def check_best_violations(violations, wizards, best_so_far_file):
    try:
        with open(best_so_far_file) as f:
            best_violations = int(f.readline().split()[0])
            if violations < best_violations:
                best_list = [str(violations)] + wizards
                print("Found Better List " + str(best_list))
                utils.write_output(best_so_far_file, best_list)
    except:
        best_list = [str(violations)] + wizards
        utils.write_output(best_so_far_file, best_list)

def solve(wizards, constraints, best_so_far_file):
    constraint_map = utils.get_constraint_map(constraints)
    violations = utils.check_violations(wizards, constraint_map)

    sorted_wizards = utils.sort_wizards(wizards, constraint_map)
    random.shuffle(sorted_wizards)

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
    print("\nSolution Sequence" + str(sequence))
    return wizards


def run(inputfile, outputfile, best_so_far_file):
    num_wizards, num_constraints, wizards, constraints = utils.read_input(inputfile)
    solution = solve(wizards, constraints, best_so_far_file)
    print("\nFound Solution")
    print(solution)
    utils.write_output(outputfile, solution)


def run_phase2_inputs(number, i):
    start_time = time.time()
    input_file = 'phase2_inputs/inputs' + number + '/input' + number + '_' + str(i) + '.in'
    output_file = 'phase2_inputs/inputs' + number + '/output' + number + '_' + str(i) + '.out'
    best_so_far_file = 'phase2_inputs/inputs' + number + '/input' + number + '_' + str(i) + '_best_so_far' + '.in'

    print("\nBeginning " + 'input' + number + '_' + str(i))
    run(input_file, output_file, best_so_far_file)
    print('Elapsed time for ' + 'input' + number + '_' + str(i) + ": " + str(time.time() - start_time))


def multi_process(num_inputs, to_do):
    cpus_to_use = multiprocessing.cpu_count()

    p = multiprocessing.Pool(cpus_to_use)
    m = multiprocessing.Manager()

    for i in range(cpus_to_use):
        p.apply_async(run_phase2_inputs, (num_inputs, to_do))
    p.close()



# Multiprocessing
if __name__ == "__main__":

    # to_do_list_20 = [3]
    # to_do_list_20 = [3]
    # to_do_list_35 = []
    # to_do_list_50 = [0, 8, 9]

    cpus_to_use = multiprocessing.cpu_count()

    p = multiprocessing.Pool(cpus_to_use)
    m = multiprocessing.Manager()

    event = m.Event()

    p.apply_async(run_phase2_inputs, ('50', 0))

    p.apply_async(run_phase2_inputs, ('50', 0))

    p.apply_async(run_phase2_inputs, ('50', 8))

    p.apply_async(run_phase2_inputs, ('50', 8))

    p.apply_async(run_phase2_inputs, ('50', 9))

    p.apply_async(run_phase2_inputs, ('50', 9))

    p.apply_async(run_phase2_inputs, ('20', 3))

    p.apply_async(run_phase2_inputs, ('20', 3))

    event.wait()
    p.close()

# run_phase2_inputs('35', [])
# run_phase2_inputs('50', [2, 8, 9])
# run_phase2_inputs('20', [3])
