from collections import Counter
from itertools import product

TIME = 1000000000


def show(data):

    x_max = max(k[0] for k in data)
    y_max = max(k[1] for k in data)

    for i in range(x_max+1):
        row = []
        for j in range(y_max+1):
            row.append(data[(i, j)])
        print(''.join(row))
    print('\n')


def neighbours(data, i, j):

    n = Counter()

    for x, y in product([-1, 0, 1], repeat=2):
        if (x, y) == (0, 0):
            continue
        ii = i + x
        jj = j + y
        n[data.get((ii, jj), ':')] += 1

    return n


def solve(data):

    # it cycles every 29 steps
    cycle = []
    found = False
    for epoch in range(TIME):

        # we have a cycle - no need to simulate
        if found:
            era = (TIME - epoch) % 28
            era -= 1
            return cycle[era]

        new_data = {}

        for (i, j), v in data.items():
            n = neighbours(data, i, j)
            if v == '.':
                # An open acre will become filled with trees if three or more adjacent acres contained trees.
                # Otherwise, nothing happens.
                new_data[(i, j)] = '|' if n['|'] >= 3 else '.'
                continue

            if v == '|':
                # An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards.
                # Otherwise, nothing happens.
                new_data[(i, j)] = '#' if n['#'] >= 3 else '|'
                continue

            if v == '#':
                # An acre containing a lumberyard will remain a lumberyard if it was adjacent to
                # at least one other lumberyard and at least one acre containing trees. Otherwise, it becomes open.
                new_data[(i, j)] = '#' if ((n['#'] >= 1) and (n['|'] >= 1)) else '.'
                continue

        data = dict(new_data)
        solution = sum(1 for v in data.values() if v == '|')
        solution *= sum(1 for v in data.values() if v == '#')

        cycle.append(solution)
        if len(cycle) > 56:
            cycle.pop(0)

        # cycle detected
        if cycle[:28] == cycle[28:]:
            found = True
            cycle = cycle[:28]


def main():

    with open("input") as in_f:
        data = {}

        for i, row in enumerate(in_f):
            if len(row) < 1:
                continue
            for j, c in enumerate(row.strip()):
                data[(i, j)] = c

    solution = solve(data)

    print(solution)


if __name__ == "__main__":

    main()
