
def solve(recipes):

    size = recipes + 10

    state = [3, 7]
    a = 0
    b = 1

    while len(state) < size:
        mix = state[a] + state[b]

        if mix > 9:
            state.append(mix // 10)
        state.append(mix % 10)

        a += (1 + state[a])
        a = a % len(state)
        b += (1 + state[b])
        b = b % len(state)

    solution = ''.join(map(str, state[recipes:recipes+10]))

    return solution


def main():

    with open("input") as in_f:
        n = int(in_f.read().strip())

    solution = solve(n)

    print(solution)


if __name__ == "__main__":

    main()
