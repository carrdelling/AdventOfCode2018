from collections import defaultdict
from copy import deepcopy

steps = defaultdict(set)
available = set()

solution = ""

with open('input_data') as in_f:
    for row in in_f:
        before, after = row[5], row[-13] if row[-13] != " " else row[-12]
        steps[after].add(before)
        available.discard(after)

        if before not in steps:
            available.add(before)

sim_available = {x for x in available}
sim_steps = deepcopy(steps)

while available:
    _next = sorted(available)[0]
    solution += _next

    rules = list(steps.items())
    for after, pre in rules:
        if _next in pre:
            pre.discard(_next)
            if not pre:
                available.add(after)
                del steps[after]

    available.discard(_next)

# now do a simulation for the second part
time = 0
n_workers = 5
workers = {i: None for i in range(n_workers)}

while sim_available or sim_steps:

    done_pieces = set()
    for _id in range(n_workers):
        if workers[_id] is None:
            if sim_available:
                piece = sorted(sim_available)[0]
                sim_available.discard(piece)
                cost = 60 + (ord(piece) - ord('A'))
                workers[_id] = [piece, cost]
        else:
            workers[_id][1] -= 1
            if workers[_id][1] == 0:
                piece_done = workers[_id][0]
                workers[_id] = None
                done_pieces.add(piece_done)

    # careful: update available pieces only after all workers spent their turn
    for piece_done in done_pieces:
        rules = list(sim_steps.items())
        for after, pre in rules:
            if piece_done in pre:
                pre.discard(piece_done)
                if not pre:
                    sim_available.add(after)
                    del sim_steps[after]
    time += 1

# let the last worker finish
ttf = 0
for _id in range(n_workers):
    if workers[_id] is not None:
        ttf = max(ttf, workers[_id][1])
time += ttf

print(f'P7-1: {solution}')
print(f'P7-2: {time}')
