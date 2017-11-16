import random
import utils
import datetime
import time
import multiprocessing


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


def solve(wizards, constraints, event):
    constraint_map = utils.get_constraint_map(constraints)
    violations = utils.check_violations(wizards, constraint_map)

    sorted_wizards = utils.sort_wizards(wizards, constraint_map)
    random.shuffle(sorted_wizards)

    sequence = [violations]
    while violations > 0:
        starting_violations = violations

        for wizard in sorted_wizards:
            violations, wizards = place_in_best_location(violations, wizard, wizards, constraint_map)

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


def run(inputfile, outputfile, event):
    num_wizards, num_constraints, wizards, constraints = utils.read_input(inputfile)
    solution = solve(wizards, constraints, event)
    print("\nFound Solution")
    print(solution)
    utils.write_output(outputfile, solution)



def run_phase2_inputs(number, i, event):
    start_time = time.time()
    print("\nBeginning " + 'input' + number + '_' + str(i))
    run('phase2_inputs/inputs' + number + '/input' + number + '_' + str(i) + '.in',
        'phase2_inputs/inputs' + number + '/output' + number + '_' + str(i) + '.out', event)
    print('Elapsed time for ' + 'input' + number + '_' + str(i) + ": " + str(time.time() - start_time))


def multi_process(num_inputs, to_do):
    cpus_to_use = multiprocessing.cpu_count()

    p = multiprocessing.Pool(cpus_to_use)
    m = multiprocessing.Manager()
    event = m.Event()

    for i in range(cpus_to_use):
        p.apply_async(run_phase2_inputs, (num_inputs, to_do, event))
    p.close()

    event.wait()
    p.terminate()

# Multiprocessing
if __name__ == "__main__":

    to_do_list_20 = [3]
    to_do_list_35 = []
    to_do_list_50 = [0,1,2,3,4,8,9]

    for i in to_do_list_20:
        multi_process("20", i)

    for i in to_do_list_35:
        multi_process("35", i)

    for i in to_do_list_50:
        multi_process("50", i)


# run_phase2_inputs('35', [])
# run_phase2_inputs('50', [2, 8, 9])
# run_phase2_inputs('20', [3])
