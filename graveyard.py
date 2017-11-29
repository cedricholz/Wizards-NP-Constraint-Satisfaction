import argparse
import utils
import random


def solve(wizards, constraints, event, best_so_far_file):
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
    constraint_ordering = wizards[:]
    constraint_map = utils.get_constraint_map(constraints)

    violations = utils.check_total_violations(wizards, constraint_map)
    sequence = [violations]
    best_found = sys.maxsize
    count = 0

    while violations > 0:

        starting_violations = violations

        # Choose a random wizard or the most constrained wizard
        random_or_most_constrained_val = random.randrange(0, 100)
        if random_or_most_constrained_val < 20:
            wizard = random.choice(constraint_ordering)
        else:
            constraint_ordering = utils.sort_wizards(wizards, constraint_map)
            wizard = constraint_ordering[0]

        # Place chosen wizard a random location, or the best location
        random_or_best_location_val = random.randrange(0, 100)
        if random_or_best_location_val < 0:
            violations, wizards = place_in_random_location(wizard, wizards, constraint_map)
        else:
            violations, wizards = place_in_best_location(violations, wizard, wizards, constraint_map)

        # Shuffle or don't
        # shuffle_or_not = random.randrange(0, 100)
        # if shuffle_or_not < 10:
        #     random.shuffle(wizards)
        #
        # sequence.append(violations)
        #
        # print(violations)

        if starting_violations == violations:
            count += 1
            if count >= 10:
                print(violations)
                random.shuffle(wizards)
                violations = utils.check_total_violations(wizards, constraint_map)
                sequence = [violations]
                count = 0

                # print("Sequence: " + str(sequence))
                # print("Stuck at " + str(violations) + " violations")
                # print(wizards)
        else:
            count = 0

    event.set()
    print("\nSolution Sequence" + str(sequence))
    return wizards

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

# def solve(wizards, constraints, event, best_so_far_file):
#     """
#     Takes an ordering of wizards, and one by one
#     (most constrained first) places them in the location
#     that causes the least amount of constraint violations.
#     If it gets stuck at a place where no single move
#     decreases the amount of violations, it shuffles
#     the ordering and starts again.
#
#     Input:
#         wizards: Number of constraint violations to beat
#         constraints: Constraints from inputfile
#         event: Multithreading event, when one core finds
#                A solution and event.set() is called, they
#                all stop and move on to the next input
#         best_so_far_file: name of the file containing the
#                           best ordering found so far
#     Output:
#         wizards: A valid ordering of the wizards
#     """
#     constraint_map = utils.get_constraint_map(constraints)
#     violations = utils.check_violations(wizards, constraint_map)
#
#     #constraint_ordering = utils.sort_wizards(wizards, constraint_map)
#     constraint_ordering = wizards[:]
#     random.shuffle(constraint_ordering)
#
#     sequence = [violations]
#     best_found = sys.maxsize
#     while violations > 0:
#
#         starting_violations = violations
#
#         for wizard in constraint_ordering:
#             violations, wizards = place_in_best_location(violations, wizard, wizards, constraint_map)
#
#             check_best_violations(violations, wizards, best_so_far_file)
#
#             sequence.append(violations)
#         if starting_violations == violations:
#             random.shuffle(wizards)
#             random.shuffle(constraint_ordering)
#
#             # print("Sequence: " + str(sequence))
#             # print("Stuck at " + str(violations) + " violations")
#             # print(wizards)
#             violations = utils.check_violations(wizards, constraint_map)
#             sequence = [violations]
#     event.set()
#     print("\nSolution Sequence" + str(sequence))
#     return wizards

# def run_friend_inputs(folder_name, wizard_number, event):
#     input_file = folder_name + '/input' + wizard_number + '.in'
#     output_file = folder_name + '/output' + wizard_number + '.out'
#     run(input_file, output_file, event)

# Check each best place
def get_best_locations(violations, wizard, wizards, constraint_map):
    wizards = wizards[:]
    best_cur_violations = violations
    starting_index = wizards.index(wizard)
    best_ndxs = []

    wizards.remove(wizard)

    wizards = [wizard] + wizards

    for ndx in range(len(wizards) - 1):
        if ndx != starting_index:
            temp_violations = utils.check_violations(wizards, constraint_map)
            if temp_violations == 0:
                return wizards
            if temp_violations < best_cur_violations:
                best_cur_violations = temp_violations
                best_ndxs = [ndx]
            elif temp_violations == best_cur_violations:
                best_ndxs.append(ndx)
        wizards[ndx], wizards[ndx + 1] = wizards[ndx + 1], wizards[ndx]
    return best_ndxs


def solve(wizards, constraints):
    constraint_map = utils.get_constraint_map(constraints)
    sorted_wizards = utils.sort_wizards(wizards, constraint_map)

    seen = set([])

    def helper(wizards, sorted_wizards):

        if tuple(wizards) in seen:
            return []
        seen.add(tuple(wizards))

        violations = utils.check_violations(wizards, constraint_map)
        print(violations)
        print(wizards)

        if violations == 0:
            return wizards
        for wizard in sorted_wizards:
            locations = get_best_locations(violations, wizard, wizards, constraint_map)
            if len(locations) == len(wizards):
                return locations
            for ndx in locations:
                wizard_dimension = wizards[:]
                wizard_dimension.remove(wizard)
                wizard_dimension.insert(ndx, wizard)

                sorted_dimension = sorted_wizards[:]
                sorted_dimension.remove(wizard)
                r = helper(wizard_dimension, sorted_dimension)
                if len(r) != 0:
                    return r
        return []

    r = helper(wizards, sorted_wizards, 0)

    while len(r) == 0:
        print(wizards)
        print("Shuffling")
        random.shuffle(wizards)
        r = helper(wizards, sorted_wizards, 0)

    return r


# Checks if there is a violation
def check_violates(ordered_wizards, constraint_map):
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


# Best so far. Moves the person with the most constraints first
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
    while violations > 0:
        starting_violations = violations
        for wizard in sorted_wizards:
            violations, wizards = place_in_best_location(violations, wizard, wizards, constraint_map)
        if starting_violations == violations:
            random.shuffle(wizards)
            print("Stuck at " + str(violations) + " violations")
            print(wizards)
            violations = utils.check_violations(wizards, constraint_map)
    return wizards


def swap(wizards, constraints):
    constraint_map = utils.get_constraint_map(constraints)

    violations = utils.check_violations(wizards, constraint_map)

    temp_list = wizards[:]
    while violations > 0:

        besti = 0
        bestj = 0
        for i in range(len(wizards) - 1):
            for j in range(1, len(wizards)):
                temp_list[i], temp_list[j] = temp_list[j], temp_list[i]
                temp_violations = utils.check_violations(temp_list, constraint_map)
                if temp_violations < violations:
                    besti = i
                    bestj = j
                    violations = temp_violations
                temp_list[i], temp_list[j] = temp_list[j], temp_list[i]

        if besti == bestj:
            random.shuffle(wizards)
            temp_list = wizards[:]
            print(violations)
            print(wizards)
            violations = utils.check_violations(wizards, constraint_map)
        else:
            x = violations
            wizards[besti], wizards[bestj] = wizards[bestj], wizards[besti]
            temp_list[besti], temp_list[bestj] = temp_list[bestj], temp_list[besti]
    return temp_list


# Best place each guy can go each iteration
def inserting(wizards, constraints):
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
                wizards[j], wizards[j + 1] = wizards[j + 1], wizards[j]
            wizards.pop()
            wizards.insert(best_j, cur_wizard)
            violations = best_cur_violations
        if starting_violations == violations:
            random.shuffle(wizards)
            print("Stuck at " + str(violations) + " violations")
            print(wizards)
            violations = utils.check_violations(wizards, constraint_map)
    return wizards


# Absolute best place one thing can go each iteration
def insert(wizards, constraints):
    constraint_map = utils.get_constraint_map(constraints)
    violations = utils.check_violations(wizards, constraint_map)

    while violations > 0:
        starting_violations = violations
        best_wizard = wizards[0]
        best_j = 0
        best_cur_violations = violations

        x = wizards
        for i in range(len(wizards)):
            cur_wizard = wizards[i]
            wizards.remove(cur_wizard)
            wizards = [cur_wizard] + wizards
            x = wizards

            for j in range(len(wizards) - 1):
                temp_violations = utils.check_violations(wizards, constraint_map)
                if temp_violations < best_cur_violations:
                    best_cur_violations = temp_violations
                    best_j = j
                    best_wizard = cur_wizard
                wizards[j], wizards[j + 1] = wizards[j + 1], wizards[j]
            wizards.pop()
            wizards.insert(i, cur_wizard)

        wizards.remove(best_wizard)
        wizards.insert(best_j, best_wizard)
        violations = best_cur_violations

        if starting_violations == violations:
            random.shuffle(wizards)
            print("Stuck at " + str(violations) + " violations")
            print(wizards)
            violations = utils.check_violations(wizards, constraint_map)
    return wizards


def backtracking(wizards, constraints):
    constraint_map = utils.get_constraint_map(constraints)

    map_copy = dict(constraint_map)
    wizards = utils.sort_wizards(wizards, map_copy)

    def helper(cur_list, wizards_left):
        if len(wizards_left) == 0:
            return cur_list

        for wizard in wizards_left:
            temp_list = cur_list + [wizard]
            violates = utils.check_violates(temp_list, constraint_map)
            if not violates:
                print(temp_list)
                temp_wizards = wizards_left[:]
                temp_wizards.remove(wizard)
                tested_list = helper(temp_list, temp_wizards)
                if len(tested_list) != 0:
                    return tested_list
        return []

    l = helper([], wizards)
    return l


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Constraint Solver.")
    parser.add_argument("input_file", type=str, help="___.in")
    parser.add_argument("output_file", type=str, help="___.out")
    args = parser.parse_args()

    num_wizards, num_constraints, wizards, constraints = utils.read_input(args.input_file)
    solution = solve(num_wizards, num_constraints, wizards, constraints)
    utils.write_output(args.output_file, solution)


def sort_wizards_traaaash(ws, cm):
    wizards = list(ws)
    constraint_map = dict(cm)
    sorted_list_of_wizards = []
    while len(constraint_map) > 0:
        m = 0
        name = ''
        for i in constraint_map:
            if len(constraint_map[i]) > m:
                m = len(constraint_map[i])
                name = i
                sorted_list_of_wizards.append(name)
        wizards.remove(name)
        del constraint_map[name]
    sorted_list_of_wizards += wizards

    return sorted_list_of_wizards
