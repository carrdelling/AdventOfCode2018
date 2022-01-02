from itertools import product

SEARCHES = 3
MAX_EXP = 28


def manhattan(x, y, z, xx, yy, zz):
    return abs(x - xx) + abs(y - yy) + abs(z - zz)


def evaluate(pos, bots):

    distance = abs(pos[0]) + abs(pos[1]) + abs(pos[2])
    reached = 0

    xx, yy, zz = pos

    for ((x, y, z), r) in bots:

        if manhattan(x, y, z, xx, yy, zz) <= r:
            reached += 1

    return reached, distance


def solve(bots):

    guess = 0, 0, 0
    best = 0
    best_dist = 0

    # need multiple searches to choose between local optima
    for _ in range(SEARCHES):
        for resolution in range(MAX_EXP, -1, -1):
            factor = 2 ** resolution

            # search 9 points in the map
            next_guess = guess
            for x, y, z in product([-1, 0, 1], repeat=3):

                pos = (guess[0] + (x*factor), guess[1] + (y * factor), guess[2] + (z * factor))
                score, dist = evaluate(pos, bots)

                if (score > best) or ((score == best) and best_dist > dist):
                    best = score
                    best_dist = dist

                    next_guess = pos

            guess = next_guess

    solution = best_dist
    return solution


def main():

    bots = []
    with open("input") as in_f:
        for row in in_f:
            if len(row) < 2:
                continue
            pos, r = row.strip().split(', r=')
            x, y, z = map(int, pos.split('<')[-1].split('>')[0].split(','))
            r = int(r)
            bot = ((x, y, z), r)
            bots.append(bot)

    solution = solve(bots)

    print(solution)


if __name__ == "__main__":

    main()
