from itertools import product
from collections import defaultdict


def distance(xx, yy, pp):
    return abs(xx - pp[0]) + abs(yy - pp[1])


points = []
with open('input_data') as in_f:
    for row in in_f:
        x, y = map(int, row.split(','))
        points.append((x - 40, y - 40))

xs = [i[0] for i in points]
min_x, max_x = min(xs), max(xs)
ys = [i[1] for i in points]
min_y, max_y = min(ys), max(ys)

closest = []
central_region = 0
for x, y in product(range(max_x + 3), range(max_y + 3)):

    distances = [(z, distance(x, y, points[z])) for z in range(len(points))]
    distances.sort(key=lambda x: x[1])
    close_to_all = sum(d[1] for d in distances) < 10000

    if distances[0][1] < distances[1][1]:
        closest.append((x, y, distances[0][0]))

    central_region += 1 if close_to_all else 0

areas = defaultdict(int)
restricted = set()

for x, y, coord in closest:

    if 0 < x < max_x + 2 and 0 < y < max_y + 2 and coord not in restricted:
        areas[coord] += 1
    else:
        restricted.add(coord)
        areas[coord] = -1

largest_area = sorted(areas.items(), key=lambda x: -x[1])[0][1]

print(f'P6-1: {largest_area}')
print(f'P2-1: {central_region}')
