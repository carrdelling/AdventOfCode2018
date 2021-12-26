from itertools import product


def solve(data):

    def _hun(x):
        return (x // 100) % 10

    grid = {(i, j): _hun((((i+10) * j) + data) * (i+10)) - 5 for i, j in product(range(1, 301), repeat=2)}

    best = None
    best_score = -9E99
    for i in range(1, 302 - 3):

        # first in the row
        score = sum(grid[(i+ii, 1+jj)] for ii in range(3) for jj in range(3))

        if score > best_score:
            best_score = score
            best = (i, 1)

        for j in range(2, 302 - 3):
            # slice to improve
            score -= sum(grid[(i+ii, j-1)] for ii in range(3))
            score += sum(grid[(i + ii, j+2)] for ii in range(3))

            if score > best_score:
                best_score = score
                best = (i, j)

    return best


def main():

    with open("input") as in_f:
        data = int(in_f.readline().strip())

    solution = solve(data)

    print(solution)


if __name__ == "__main__":

    main()
