GENERATIONS = 20


def solve(state, rules):

    for g in range(GENERATIONS):

        new_state = {}
        for p in range(-3, max(state)+3):

            key = ''.join([state.get(p-2, '.'), state.get(p-1, '.'), state.get(p, '.'),
                           state.get(p+1, '.'), state.get(p+2, '.')])
            new_state[p] = rules[key]

        # save the state
        state = new_state

    solution = sum(idx for idx, v in state.items() if v != '.')

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
