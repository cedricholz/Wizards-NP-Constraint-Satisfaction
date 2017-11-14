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
