import argparse
import random
import utils



def check_violations(ordered_wizards, constraint_map):
    violations = 0
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
                    violations += 1

                elif wizard2 in prev_wizards and wizard1 in next_wizards:
                    violations += 1

        prev_wizards.add(cur_wizard)
    return violations


def solve(num_wizards, num_constraints, wizards, constraints):
    """
    Write your algorithm here.
    Input:
        num_wizards: Number of wizards
        num_constraints: Number of constraints
        wizards: An array of wizard names, in no particular order
        constraints: A 2D-array of constraints, 
                     where constraints[0] may take the form ['A', 'B', 'C']i

    Output:
        An array of wizard names in the ordering your algorithm returns
    """
    constraint_map = utils.get_constraint_map(constraints)

    violations = check_violations(wizards, constraint_map)

    x = 0
    while violations > 0:
        for i in range(len(wizards)):
            best_violations = violations
            best_j = i

            cur_wizard = wizards[i]
            wizards.remove(cur_wizard)

            for j in range(len(wizards) + 1):
                if j != i:
                    wizards.insert(j, cur_wizard)
                    temp_violations = check_violations(wizards, constraint_map)
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
            violations = check_violations(wizards, constraint_map)
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

folder_name = 'Nizans'
wizard_number = '35'

run(folder_name + '/input' + wizard_number + '.in', folder_name + '/output' + wizard_number + '.out')