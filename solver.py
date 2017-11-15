import random
import utils
import datetime
import time


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


def solve(wizards, constraints):
    constraint_map = utils.get_constraint_map(constraints)
    violations = utils.check_violations(wizards, constraint_map)

    sorted_wizards = utils.sort_wizards(wizards, constraint_map)

    sequence = [violations]
    while violations > 0:
        starting_violations = violations

        for wizard in sorted_wizards:
            violations, wizards = place_in_best_location(violations, wizard, wizards, constraint_map)

            sequence.append(violations)
        if starting_violations == violations:
            random.shuffle(wizards)
            #print("Sequence: " + str(sequence))
            #print("Stuck at " + str(violations) + " violations")
            #print(wizards)
            violations = utils.check_violations(wizards, constraint_map)
            sequence = [violations]

    print("\nSolution Sequence" + str(sequence))
    return wizards


def run(inputfile, outputfile):
    num_wizards, num_constraints, wizards, constraints = utils.read_input(inputfile)
    solution = solve(wizards, constraints)
    print("\nFound Solution")
    print(solution)
    utils.write_output(outputfile, solution)


# folder_name = 'Alexs'
# wizard_number = '50'
#
# run(folder_name + '/input' + wizard_number + '.in', folder_name + '/output' + wizard_number + '.out')

def run_inputs(number, to_do_list):
    for i in range(10):
        if i in to_do_list:
            start_time = time.time()
            print("\nBeginning " + 'input' + number + '_' + str(i))
            run('phase2_inputs/inputs' + number + '/input' + number + '_' + str(i) + '.in',
                'phase2_inputs/inputs' + number + '/output' + number + '_' + str(i) + '.out')
            print('Elapsed time for ' + 'input' + number + '_' + str(i) + ": " + str(time.time()-start_time))


run_inputs('20', [3])
run_inputs('35', [5,7,8,9])
run_inputs('50', [0,1,2,3,4,5,6,7,8,9])
