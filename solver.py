import argparse
import random
import utils


def solve(num_wizards, num_constraints, wizards, constraints):
    constraint_map = utils.get_constraint_map(constraints)
    violations = utils.check_violations(wizards, constraint_map)

    x = 0
    while violations > 0:
        starting_violations = violations
        for i in range(len(wizards)):
            best_violations = violations
            best_j = i

            cur_wizard = wizards[i]
            wizards.remove(cur_wizard)

            for j in range(len(wizards) + 1):
                if j != i:
                    wizards.insert(j, cur_wizard)
                    temp_violations = utils.check_violations(wizards, constraint_map)
                    if temp_violations < best_violations:
                        best_violations = temp_violations
                        best_j = j
                    wizards.remove(cur_wizard)
            wizards.insert(best_j, cur_wizard)

            violations = best_violations
        if x == violations:
            random.shuffle(wizards)
            print(violations)
            print(wizards)
            violations = utils.check_violations(wizards, constraint_map)
        else:
            x = violations

    return wizards


def read_input(filename):
    with open(filename) as f:
        num_wizards = int(f.readline())
        num_constraints = int(f.readline())
        constraints = []
        wizards = set()
        for _ in range(num_constraints):
            c = f.readline().split()
            constraints.append(c)
            for w in c:
                wizards.add(w)

    wizards = list(wizards)
    return num_wizards, num_constraints, wizards, constraints


def write_output(filename, solution):
    with open(filename, "w") as f:
        for wizard in solution:
            f.write("{0} ".format(wizard))


def run(inputfile, outputfile):
    num_wizards, num_constraints, wizards, constraints = read_input(inputfile)
    solution = solve(num_wizards, num_constraints, wizards, constraints)
    print("\nFound Solution")
    print(solution)
    write_output(outputfile, solution)


folder_name = 'Armans'
wizard_number = '50'

run(folder_name + '/input' + wizard_number + '.in', folder_name + '/output' + wizard_number + '.out')
