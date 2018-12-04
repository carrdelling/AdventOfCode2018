from itertools import product

seen = set()
clashed = set()
single = None

patterns = []
with open('input_data') as in_f:
    for row in in_f:
        _id, _, location, size = row.strip().split()
        patterns.append((_id, location, size))

for _, location, size in patterns:

    x, y = list(map(int, location[:-1].split(',')))
    d_x, d_y = list(map(int, size.split('x')))

    x += 1
    y += 1
    for i, j in product(range(d_x), range(d_y)):
        inch = (x + i, y + j)

        if inch in seen:
            clashed.add(inch)
        else:
            seen.add(inch)

for _id, location, size in patterns:

    x, y = list(map(int, location[:-1].split(',')))
    d_x, d_y = list(map(int, size.split('x')))

    x += 1
    y += 1
    if all((x + i, y + j) not in clashed for i, j in product(range(d_x), range(d_y))):
        single = _id[1:]

print(f'P3-1: {len(clashed)}')
print(f'P3-2: {single}')
