

def manhattan(x, y, z, xx, yy, zz):
    return abs(x - xx) + abs(y - yy) + abs(z - zz)


def solve(bots):

    bots.sort(key=lambda _x: -_x[-1])

    (x, y, z), r = bots[0]

    solution = sum(1 if manhattan(x, y, z, xx, yy, zz) < r else 0 for (xx, yy, zz), _ in bots)

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
