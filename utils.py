"""
utils.py
"""

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
                print("Best violations updated: " + str(violations) + " " + best_so_far_file)
                utils.write_output(best_so_far_file, best_list)
    except:
        best_list = [str(violations)] + wizards
        utils.write_output(best_so_far_file, best_list)


def check_wizard_violations(ordered_wizards, constraint_map, wizard):
    wizard_index = ordered_wizards.index(wizard)

    if wizard_index == 0 or wizard_index == len(ordered_wizards) - 1:
        return 0

    violations = 0
    prev_wizards = set(ordered_wizards[:wizard_index])
    next_wizards = set(ordered_wizards[wizard_index + 1:])

    if wizard in constraint_map:
        cur_constraints = constraint_map[wizard]
        for constraint in cur_constraints:
            wizard1 = constraint[0]
            wizard2 = constraint[1]

            if wizard1 in prev_wizards and wizard2 in next_wizards:
                violations += 1

            elif wizard2 in prev_wizards and wizard1 in next_wizards:
                violations += 1

    return violations


def sort_wizards(ordered_wizards, constraint_map):
    wizard_tuples = []
    for wizard in ordered_wizards:
        wizard_violations = check_wizard_violations(ordered_wizards, constraint_map, wizard)
        wizard_tuples.append((wizard, wizard_violations))

    wizard_tuples.sort(key=lambda tup: tup[1])

    sorted_wizards = []
    for wizard_tup in wizard_tuples:
        sorted_wizards.append(wizard_tup[0])
    return sorted_wizards


def get_constraint_map(constraints):
    """
    Returns a mapping of the wizards
    to a list of their constraints
    Input:
        constraints: List of al the constraints

    Output:
        constraint_map: Wizard names mapped to a list of their constraits
    """
    constraint_map = {}
    for constraint in constraints:
        wizard = constraint[2]
        if wizard not in constraint_map:
            constraint_map[wizard] = [constraint[:2]]
        else:
            constraint_map[wizard].append(constraint[:2])
    return constraint_map


def check_total_violations(ordered_wizards, constraint_map):
    """
    Checks how many violations are present
    in the current wizard ordering

    Input:
        ordered_wizards: Current ordering of the wizards
        constraint_map: Wizard names mapped to a list of their constraits

    Output:
        violations: Number of violations
    """
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
