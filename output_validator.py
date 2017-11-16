# Released to students

import sys


def main(argv):
    if len(argv) != 2:
        print("Usage: python output_validator.py [path_to_input_file] [path_to_output_file]")
        return
    constraints_satisfied, num_constraints, constraints_failed = processInput(argv[0], argv[1])
    print(
        "You satisfied {}/{} constraints. List of failed constraints: {}".format(constraints_satisfied, num_constraints,
                                                                                 constraints_failed))


def processInput(input_file, output_file):
    fin = open(input_file, "r")
    fout = open(output_file, "r")

    num_wiz_in_input = int(fin.readline().split()[0])
    num_constraints = int(fin.readline().split()[0])

    output_ordering = fout.readline().split()
    output_ordering_set = set(output_ordering)
    output_ordering_map = {k: v for v, k in enumerate(output_ordering)}

    if (len(output_ordering_set) != num_wiz_in_input):
        return "Input file has unique {} wizards, but output file has {}".format(num_wiz_in_input,
                                                                                 len(output_ordering_set))

    if (len(output_ordering_set) != len(output_ordering)):
        return "The output ordering contains repeated wizards."

    # Counts how many constraints are satisfied.
    constraints_satisfied = 0
    constraints_failed = []
    for i in range(num_constraints):
        line_num = i + 4
        constraint = fin.readline().split()

        c = constraint  # Creating an alias for easy reference
        m = output_ordering_map  # Creating an alias for easy reference

        wiz_a = m[c[0]]
        wiz_b = m[c[1]]
        wiz_mid = m[c[2]]

        if (wiz_a < wiz_mid < wiz_b) or (wiz_b < wiz_mid < wiz_a):
            constraints_failed.append(c)
        else:
            constraints_satisfied += 1

    return constraints_satisfied, num_constraints, constraints_failed


def validate_file(number, i):
    input_file = 'phase2_inputs/inputs' + number + '/input' + number + '_' + str(i) + '.in'
    output_file = 'outputs/output' + number + '_' + str(i) + ".out"
    print(processInput(input_file, output_file))


numbers = ['20', '35', '50']
for n in numbers:
    for i in range(10):
        validate_file(n, i)
