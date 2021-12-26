EQ_GENERATIONS = 200
GENERATIONS = 50000000000


def solve(state, rules):

    # get to an equilibrium
    for g in range(EQ_GENERATIONS):

        new_state = {}
        for p in range(-3, max(state)+3):

            key = ''.join([state.get(p-2, '.'), state.get(p-1, '.'), state.get(p, '.'),
                           state.get(p+1, '.'), state.get(p+2, '.')])
            new_state[p] = rules[key]

        # save the state
        state = new_state

    # see where the plants are now
    solution = sum(idx for idx, v in state.items() if v != '.')

    # also count how many plants
    count = sum(1 for v in state.values() if v != '.')

    # every new generation just shifts the plants by one
    solution += ((GENERATIONS - EQ_GENERATIONS) * count)

    return solution


def main():

    with open("input") as in_f:
        state = {idx: c for idx, c in enumerate(in_f.readline().strip().split()[-1])}
        rules = {}

        for row in in_f:

            if len(row) < 3:
                continue

            k, v = row.strip().split(' => ')
            rules[k] = v

    solution = solve(state, rules)

    print(solution)


if __name__ == "__main__":

    main()
