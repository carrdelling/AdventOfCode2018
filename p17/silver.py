

def show(_earth):

    earth = {}

    for k, v in _earth.items():
        earth[k] = v

    x_min = min(k[0] for k in earth) - 1
    x_max = max(k[0] for k in earth) + 1
    y_min = min(k[1] for k in earth)
    y_max = max(k[1] for k in earth) + 1

    for y in range(y_min, y_max):
        row = []
        for x in range(x_min, x_max):
            s = earth.get((x, y), '.')
            row.append(s)
        print(''.join(row))


def solve(data):

    # build earth
    earth = build_earth(data)

    max_y = max(k[1] for k in earth)
    min_y = min(k[1] for k, v in earth.items() if v == '#')

    flow(earth)

    show(earth)

    solution = sum(1 for k, x in earth.items() if x == 'X' and (min_y <= k[1] <= max_y))

    return solution


def pressure_left(earth, x, y):

    while True:

        if earth.get((x, y), '.') == '.':
            return False
        if earth.get((x, y), '.') == '#':
            return True

        x -= 1


def pressure_right(earth, x, y):
    while True:

        if earth.get((x, y), '.') == '.':
            return False
        if earth.get((x, y), '.') == '#':
            return True

        x += 1


def pressure_both(earth, x, y):

    return all([pressure_left(earth, x-1, y), pressure_right(earth, x+1, y)])


def flow(earth):

    y_max = max(k[1] for k in earth)

    queue = [(500, 0)]

    while queue:

        s = queue.pop()
        x, y = s
        new_states = []
        changed = False

        # flow down
        if earth.get((x, y+1), '.') == '.' and y < y_max:
            earth[(x, y+1)] = 'X'
            changed = True
            new_states.append((x, y+1))

        # flow left
        if (earth.get((x, y+1), '.') in {'X', '#'}) and (earth.get((x-1, y+1), '.') in {'X', '#'}) and (
                earth.get((x-1, y), '.') not in {'X', '#'}) and (pressure_both(earth, x, y+1)):
            earth[(x-1, y)] = 'X'
            changed = True
            new_states.append((x-1, y))
        # flow left-down
        elif (earth.get((x-1, y), '.') == '.' and earth.get((x-1, y+1), '.') == '.' and
              earth.get((x, y+1), '.') == '#'):
            earth[(x-1, y)] = 'X'
            changed = True
            new_states.append((x-1, y))
        # flow right
        if (earth.get((x, y+1), '.') in {'X', '#'}) and (earth.get((x+1, y+1), '.') in {'X', '#'}) and (
                earth.get((x+1, y), '.') not in {'X', '#'}) and (pressure_both(earth, x, y+1)):
            earth[(x+1, y)] = 'X'
            changed = True
            new_states.append((x+1, y))
        # flow right-down
        elif (earth.get((x+1, y), '.') == '.' and earth.get((x+1, y+1), '.') == '.' and
              earth.get((x, y+1), '.') == '#'):
            earth[(x+1, y)] = 'X'
            changed = True
            new_states.append((x+1, y))

        if changed:
            queue.append(s)
        if new_states:
            queue += new_states


def build_earth(data):

    earth = {}
    for c, p, _, s, e in data:
        if c == 'x':
            for i in range(s, e + 1):
                earth[(p, i)] = '#'
        else:
            for i in range(s, e + 1):
                earth[(i, p)] = '#'
    earth[(500, 0)] = '+'
    return earth


def main():

    with open("input") as in_f:
        cases = []

        for row in in_f:
            if len(row) < 1:
                continue
            first, second = row.split(', ')
            t, point = first.split('=')
            s, points = second.split('=')
            p1, p2 = map(int, points.split('..'))
            case = (t, int(point), s, p1, p2)

            cases.append(case)

    solution = solve(cases)

    print(solution)


if __name__ == "__main__":

    main()
