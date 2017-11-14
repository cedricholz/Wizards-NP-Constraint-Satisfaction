import argparse
import random

"""
======================================================================
  Complete the following function.
======================================================================
"""
def check_violates(ordered_wizards, constraint_map):
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
                    return True

                elif wizard2 in prev_wizards and wizard1 in next_wizards:
                    return True

        prev_wizards.add(cur_wizard)
    return False


def sort_wizards(wizards, constraint_map):
    print(constraint_map)
    l = []
    while len(constraint_map) > 0:
        m = 0
        name = ''
        for i in constraint_map:
            if len(constraint_map[i]) > m:
                m = len(constraint_map[i])
                name = i
        l.append(name)
        wizards.remove(name)
        del constraint_map[name]
    l += wizards
    return l

def get_constraint_map(constraints):
    d = {}
    for constraint in constraints:
        wizard = constraint[2]
        if wizard not in d:
            d[wizard] = [constraint[:2]]
        else:
            d[wizard].append(constraint[:2])
    return d


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
    constraint_map = get_constraint_map(constraints)

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



"""
======================================================================
   No need to change any code below this line
======================================================================
"""


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Constraint Solver.")
    parser.add_argument("input_file", type=str, help="___.in")
    parser.add_argument("output_file", type=str, help="___.out")
    args = parser.parse_args()

    num_wizards, num_constraints, wizards, constraints = read_input(args.input_file)
    solution = solve(num_wizards, num_constraints, wizards, constraints)
    write_output(args.output_file, solution)



# def swap(num_wizards, num_constraints, wizards, constraints):
#     constraint_map = get_constraint_map(constraints)
#
#     violations = check_violations(wizards, constraint_map)
#
#     temp_list = wizards[:]
#     while violations > 0:
#
#         besti = 0
#         bestj = 0
#         for i in range(len(wizards) - 1):
#             for j in range(1, len(wizards)):
#                 temp_list[i], temp_list[j] = temp_list[j], temp_list[i]
#                 temp_violations = check_violations(temp_list, constraint_map)
#                 if temp_violations < violations:
#                     besti = i
#                     bestj = j
#                     violations = temp_violations
#                 temp_list[i], temp_list[j] = temp_list[j], temp_list[i]
#
#         wizards[besti], wizards[bestj] = wizards[bestj], wizards[besti]
#         temp_list[besti], temp_list[bestj] = temp_list[bestj], temp_list[besti]
#     return temp_list
#
# def inserting(num_wizards, num_constraints, wizards, constraints):
#     constraint_map = get_constraint_map(constraints)
#
#     violations = check_violations(wizards, constraint_map)
#
#     while violations > 0:
#         for i in range(len(wizards)):
#             best_violations = violations
#             best_j = i
#
#             cur_wizard = wizards[i]
#             wizards.remove(cur_wizard)
#
#             for j in range(len(wizards) + 1):
#                 if j != i:
#                     wizards.insert(j, cur_wizard)
#                     temp_violations = check_violations(wizards, constraint_map)
#                     if temp_violations < best_violations:
#                         best_violations = temp_violations
#                         best_j = j
#                     wizards.remove(cur_wizard)
#             wizards.insert(best_j, cur_wizard)
#
#             violations = best_violations
#     return wizards


# def naive(num_wizards, num_constraints, wizards, constraints):
#     constraint_map = get_constraint_map(constraints)
#
#     map_copy = dict(constraint_map)
#     wizards = sort_wizards(wizards, map_copy)[::-1]
#
#     def helper(cur_list, wizards_left):
#         if len(wizards_left) == 0:
#             return cur_list
#
#         for wizard in wizards_left:
#             temp_list = cur_list + [wizard]
#             violates = check_violates(temp_list, constraint_map)
#             if not violates:
#                 print(temp_list)
#                 temp_wizards = wizards_left[:]
#                 temp_wizards.remove(wizard)
#                 tested_list = helper(temp_list, temp_wizards)
#                 if len(tested_list) != 0:
#                     return tested_list
#         return []
#
#     l = helper([], wizards)
#     return l