from itertools import product


def print_grid(g, i, j):

    for x in range(1, i):
        r = []
        for y in range(1, j):
            r.append(g[(x, y)])
        print(r)


def solve(data):

    def _hun(x):
        return (x // 100) % 10

    grid = {(i, j): _hun((((i+10) * j) + data) * (i+10)) - 5 for i, j in product(range(1, 301), repeat=2)}

    # fill sums
    sums = {}
    for i, j in product(range(1, 301), repeat=2):
        v = grid[(i, j)]
        v += sums.get((i, j-1), 0)
        v += sums.get((i-1, j), 0)
        v -= sums.get((i - 1, j-1), 0)
        sums[(i, j)] = v

    best_grid = None
    best = -9E99
    for size in range(1, 300):
        for i, j in product(range(1, 302 - size), repeat=2):
            v = sums[(i-1+size, j-1+size)]
            v += sums.get((i-1, j-1), 0)
            v -= sums.get((i-1+size, j-1), 0)
            v -= sums.get((i-1, j-1+size), 0)

            if v > best:
                best = v
                best_grid = (i, j, size)

    return best_grid


def main():

    with open("input") as in_f:
        data = int(in_f.readline().strip())

    solution = solve(data)

    print(solution)


if __name__ == "__main__":

    main()
