# Released to students

import sys

def main(argv):
    if len(argv) != 2:
        print("Usage: python output_validator.py [path_to_input_file] [path_to_output_file]")
        return
    constraints_satisfied, num_constraints, constraints_failed = processInput(argv[0], argv[1])
    print("You satisfied {}/{} constraints. List of failed constraints: {}".format(constraints_satisfied, num_constraints, constraints_failed))

def processInput(input_file, output_file):
    fin = open(input_file, "r")
    fout = open(output_file, "r")

    num_wiz_in_input = int(fin.readline().split()[0])
    input_wizard_set = set(fin.readline().split())
    num_constraints = int(fin.readline().split()[0])

    output_ordering = fout.readline().split()
    output_ordering_set = set(output_ordering)
    output_ordering_map = {k: v for v, k in enumerate(output_ordering)}


    if (len(output_ordering_set) != num_wiz_in_input):
        return "Input file has unique {} wizards, but output file has {}".format(num_wiz_in_input, len(output_ordering_set))

    if (len(output_ordering_set) != len(output_ordering)):
        return "The output ordering contains repeated wizards."

    if (input_wizard_set != output_ordering_set):
        return "The output ordering contains wizards that are different from the ones in the input ordering."

    # Counts how many constraints are satisfied.
    constraints_satisfied = 0
    constraints_failed = []
    for i in range(num_constraints):
        line_num = i + 4
        constraint = fin.readline().split()

        c = constraint # Creating an alias for easy reference
        m = output_ordering_map # Creating an alias for easy reference

        wiz_a = m[c[0]]
        wiz_b = m[c[1]]
        wiz_mid = m[c[2]]

        if (wiz_a < wiz_mid < wiz_b) or (wiz_b < wiz_mid < wiz_a):
            constraints_failed.append(c)
        else:
            constraints_satisfied += 1

    return constraints_satisfied, num_constraints, constraints_failed

if __name__ == '__main__':
    main(sys.argv[1:])
