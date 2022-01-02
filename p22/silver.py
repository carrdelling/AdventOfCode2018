from itertools import product


def show(risk, tx, ty):

    for j in range(ty+1):
        row = []
        for i in range(tx+1):
            s = {0: '.', 1: '=', 2: '|'}
            row.append(s[risk[(i, j)]])
        print(''.join(row))


def solve(depth, tx, ty):

    geologic = {}
    erosion = {}

    for i in range(tx + 1):
        geologic[(i, 0)] = i * 16807
        erosion[(i, 0)] = (geologic[(i, 0)] + depth) % 20183

    for j in range(ty + 1):
        geologic[(0, j)] = j * 48271
        erosion[(0, j)] = (geologic[(0, j)] + depth) % 20183

    for i, j in product(range(1, tx+1), range(1, ty+1)):
        geologic[(i, j)] = erosion[(i-1, j)] * erosion[(i, j-1)]
        erosion[(i, j)] = (geologic[(i, j)] + depth) % 20183

    geologic[(0, 0)] = 0
    geologic[(tx, ty)] = 0
    erosion[(0, 0)] = 0
    erosion[(tx, ty)] = 0

    risk = {k: v % 3 for k, v in erosion.items()}
    solution = sum(v for v in risk.values())

    show(risk, tx, ty)

    return solution


def main():

    with open("input") as in_f:
        d = int(in_f.readline().strip().split()[-1])
        tx, ty = map(int, in_f.readline().strip().split()[-1].split(','))

    solution = solve(d, tx, ty)

    print(solution)


if __name__ == "__main__":

    main()
