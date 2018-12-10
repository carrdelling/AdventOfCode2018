

def compute_areas(state):

    possible_areas = []
    for step in range(20000):

        min_x, max_x = 10000, 0
        min_y, max_y = 10000, 0

        for x, y, v_x, v_y in state:
            min_x = min(min_x, x + step * v_x)
            max_x = max(max_x, x + step * v_x)
            min_y = min(min_y, y + step * v_y)
            max_y = max(max_y, y + step * v_y)
        size_box = max_x - min_x + max_y - min_y
        possible_areas.append([max_x, min_x, max_y, min_y, step, size_box])

    return possible_areas


def build_grid(area, state):

    max_x, min_x, max_y, min_y, step, size_box = area

    grid_x = max_x - min_x + 1

    grid = [[' '] * grid_x for _ in range(min_y, max_y + 1)]

    for x, y, vx, vy in state:
        _y = y + step * vy - min_y
        _x = x + step * vx - min_x
        grid[_y][_x] = '*'

    return grid


current_state = []
with open('input_data') as in_f:
    for row in in_f:
        pos, vel = row.strip().split('<')[1:3]

        pos_x, pos_y = map(int, pos.split('>')[0].split(','))
        vel_x, vel_y = map(int, vel.split('>')[0].split(','))

        current_state.append([pos_x, pos_y, vel_x, vel_y])

# pick the moment at which the area is smaller
areas = compute_areas(current_state)
areas.sort(key=lambda x: x[-1])

grid = build_grid(areas[0], current_state)

print(f'P10-1: \n\n')
for row in grid:
    print(''.join(row))
print('\n')

print(f'P10-2: {areas[0][-2]}')
