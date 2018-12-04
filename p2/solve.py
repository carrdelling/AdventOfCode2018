from collections import Counter

has_two = 0
has_three = 0
seen = set()

solution = None
with open('input_data') as in_f:
    for row in in_f:
        _id = row.strip()
        counts = Counter(_id)
        has_two += 1 if any(c == 2 for c in counts.values()) else 0
        has_three += 1 if any(c == 3 for c in counts.values()) else 0

        if solution is None:
            for old in seen:
                difference = -1
                for idx, (c, cc) in enumerate(zip(old, _id)):
                    if c != cc:
                        if difference < 0:
                            difference = idx
                        else:
                            break
                else:
                    solution = old[:difference] + old[difference+1:]

        seen.add(_id)

print(f'P2-1: {has_two * has_three}')
print(f'P2-2: {solution}')
