
def solve(recipes):

    pattern = [int(c) for c in str(recipes)]
    size = len(pattern)

    state = [3, 7]
    a = 0
    b = 1

    while True:

        mix = state[a] + state[b]

        if mix > 9:
            state.append(mix // 10)

            test = state[-size:]

            if test == pattern:
                break

        state.append(mix % 10)

        test = state[-size:]

        if test == pattern:
            break

        # update after checking
        a += (1 + state[a])
        a = a % len(state)
        b += (1 + state[b])
        b = b % len(state)

    solution = len(state) - size

    return solution


def main():

    with open("input") as in_f:
        n = int(in_f.read().strip())

    solution = solve(n)

    print(solution)


if __name__ == "__main__":

    main()
