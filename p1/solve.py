frequencies = []

with open('input_data') as in_f:
    for row in in_f:
        val = int(row.strip())
        frequencies.append(val)

seen = set()
current = 0
seen.add(current)

idx = 0
while True:
    current += frequencies[idx]

    if current in seen:
        break
    seen.add(current)
    idx = (idx + 1) % len(frequencies)

print(f'1_1: {sum(frequencies)}')
print(f'1_2: {current}')
