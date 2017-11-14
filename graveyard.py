# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Constraint Solver.")
#     parser.add_argument("input_file", type=str, help="___.in")
#     parser.add_argument("output_file", type=str, help="___.out")
#     args = parser.parse_args()
#
#     num_wizards, num_constraints, wizards, constraints = read_input(args.input_file)
#     solution = solve(num_wizards, num_constraints, wizards, constraints)
#     write_output(args.output_file, solution)


# def swap(num_wizards, num_constraints, wizards, constraints):
#     constraint_map = utils.get_constraint_map(constraints)
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
#         if besti == bestj:
#             random.shuffle(wizards)
#             temp_list = wizards[:]
#             print(violations)
#             print(wizards)
#             violations = check_violations(wizards, constraint_map)
#         else:
#             x = violations
#             wizards[besti], wizards[bestj] = wizards[bestj], wizards[besti]
#             temp_list[besti], temp_list[bestj] = temp_list[bestj], temp_list[besti]
#     return temp_list




#Best place each guy can go each move
# def inserting(num_wizards, num_constraints, wizards, constraints):
#     constraint_map = utils.get_constraint_map(constraints)
#     violations = utils.check_violations(wizards, constraint_map)
#
#     while violations > 0:
#         starting_violations = violations
#         for i in range(len(wizards)):
#             best_cur_violations = violations
#             best_j = i
#
#             cur_wizard = wizards[i]
#             wizards.remove(cur_wizard)
#             wizards = [cur_wizard] + wizards
#
#             for j in range(len(wizards) - 1):
#                 temp_violations = utils.check_violations(wizards, constraint_map)
#                 if temp_violations <= best_cur_violations:
#                     best_cur_violations = temp_violations
#                     best_j = j
#                 wizards[j], wizards[j+1] = wizards[j+1], wizards[j]
#             wizards.pop()
#             wizards.insert(best_j, cur_wizard)
#             violations = best_cur_violations
#         if starting_violations == violations:
#             random.shuffle(wizards)
#             print("Stuck at " + str(violations) + " violations")
#             print(wizards)
#             violations = utils.check_violations(wizards, constraint_map)
#     return wizards


#Absolute best place anything can go each move
# def insert(wizards, constraints):
#     constraint_map = utils.get_constraint_map(constraints)
#     violations = utils.check_violations(wizards, constraint_map)
#
#     while violations > 0:
#         starting_violations = violations
#         best_wizard = wizards[0]
#         best_j = 0
#         best_cur_violations = violations
#
#         x = wizards
#         for i in range(len(wizards)):
#             cur_wizard = wizards[i]
#             wizards.remove(cur_wizard)
#             wizards = [cur_wizard] + wizards
#             x = wizards
#
#             for j in range(len(wizards) - 1):
#                 temp_violations = utils.check_violations(wizards, constraint_map)
#                 if temp_violations < best_cur_violations:
#                     best_cur_violations = temp_violations
#                     best_j = j
#                     best_wizard = cur_wizard
#                 wizards[j], wizards[j + 1] = wizards[j + 1], wizards[j]
#             wizards.pop()
#             wizards.insert(i, cur_wizard)
#
#         wizards.remove(best_wizard)
#         wizards.insert(best_j, best_wizard)
#         violations = best_cur_violations
#
#         if starting_violations == violations:
#             random.shuffle(wizards)
#             print("Stuck at " + str(violations) + " violations")
#             print(wizards)
#             violations = utils.check_violations(wizards, constraint_map)
#     return wizards



# def backtracking(num_wizards, num_constraints, wizards, constraints):
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
