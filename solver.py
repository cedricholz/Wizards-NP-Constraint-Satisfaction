import random
import utils


def solve(wizards, constraints):
    constraint_map = utils.get_constraint_map(constraints)
    violations = utils.check_violations(wizards, constraint_map)


    while violations > 0:
        starting_violations = violations
        for i in range(len(wizards)):
            best_cur_violations = violations
            best_j = i

            cur_wizard = wizards[i]
            wizards.remove(cur_wizard)
            wizards = [cur_wizard] + wizards

            for j in range(len(wizards) - 1):
                temp_violations = utils.check_violations(wizards, constraint_map)
                if temp_violations <= best_cur_violations:
                    best_cur_violations = temp_violations
                    best_j = j
                wizards[j], wizards[j+1] = wizards[j+1], wizards[j]
            wizards.pop()
            wizards.insert(best_j, cur_wizard)
            violations = best_cur_violations
        if starting_violations == violations:
            random.shuffle(wizards)
            print("Stuck at " + str(violations) + " violations")
            print(wizards)
            violations = utils.check_violations(wizards, constraint_map)
    return wizards


def run(inputfile, outputfile):
    num_wizards, num_constraints, wizards, constraints = utils.read_input(inputfile)
    solution = solve(wizards, constraints)
    print("\nFound Solution")
    print(solution)
    utils.write_output(outputfile, solution)


folder_name = 'Keerthis'
wizard_number = '35'

run(folder_name + '/input' + wizard_number + '.in', folder_name + '/output' + wizard_number + '.out')
