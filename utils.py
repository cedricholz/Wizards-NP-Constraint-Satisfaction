"""
utils.py
"""

"""
Sorts the wizards based on their
number of constraints

Input:
    ws: Current ordering of the wizards
    cm: Wizard names mapped to a list of their constraits

Output:
    sorted_list_of_wizards: the sorted list of wizards
"""


def sort_wizards(ws, cm):
    wizards = set(ws)
    constraint_map = dict(cm)
    contraint_tups = []

    for i in constraint_map:
        contraint_tups.append((i, len(constraint_map[i])))
        wizards.remove(i)
    for i in wizards:
        contraint_tups.append((i, 0))

    contraint_tups.sort(key=lambda tup: tup[1], reverse = True)

    sorted_wizards = []
    for i in contraint_tups:
        sorted_wizards.append(i[0])
    return sorted_wizards


"""
Returns a mapping of the wizards
to a list of their constraints
Input:
    constraints: List of al the constraints
    
Output:
    constraint_map: Wizard names mapped to a list of their constraits
"""


def get_constraint_map(constraints):
    constraint_map = {}
    for constraint in constraints:
        wizard = constraint[2]
        if wizard not in constraint_map:
            constraint_map[wizard] = [constraint[:2]]
        else:
            constraint_map[wizard].append(constraint[:2])
    return constraint_map


"""
Checks how many violations are present
in the current wizard ordering

Input:
    ordered_wizards: Current ordering of the wizards
    constraint_map: Wizard names mapped to a list of their constraits

Output:
    violations: Number of violations
"""


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
