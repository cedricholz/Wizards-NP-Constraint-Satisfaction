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


def sort_wizards(wizards, constraint_map):
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

