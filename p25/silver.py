from itertools import product


def is_close(a, b):

    w, x, y, z = a
    ww, xx, yy, zz = b

    return (abs(w-ww) + abs(x - xx) + abs(y - yy) + abs(z - zz)) <= 3


def close(ca, cb):

    for a, b in product(ca, cb):
        if is_close(a, b):
            return True
    return False


def solve(points):

    # first pass
    clusters = [[points[0]]]

    for p in points[1:]:
        join_to = -1
        for idx in range(len(clusters)):

            if join_to > -1:
                continue
            for t in clusters[idx]:
                if join_to > -1:
                    continue
                if is_close(p, t):
                    join_to = idx
        if join_to > -1:
            clusters[join_to].append(p)
        else:
            clusters.append([p])

    # converge
    change = True

    while change:
        old_len = len(clusters)
        change = False

        for idx, idx2 in product(range(len(clusters)), repeat=2):

            if idx == idx2:
                continue
            if len(clusters[idx]) * len(clusters[idx]) == 0:
                continue
            if close(clusters[idx], clusters[idx2]):
                clusters[idx] += clusters[idx2]
                clusters[idx2] = []

        clusters = [ c for c in clusters if len(c) > 0]

        if old_len > len(clusters):
            change = True

    return len(clusters)


def main():

    points = []
    with open("input") as in_f:
        for row in in_f:
            if len(row) < 2:
                continue
            p = tuple(map(int, row.strip().split(',')))
            points.append(p)

    solution = solve(points)

    print(solution)


if __name__ == "__main__":

    main()
