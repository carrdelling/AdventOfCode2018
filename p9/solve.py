from collections import defaultdict, deque

with open('input_data') as in_f:
    data = next(in_f).split()
    players, marbles = int(data[0]), int(data[-2])

board = deque([0])
scores = defaultdict(int)
current = 0
current_player = 0

for marble in range(1, (marbles * 100)+1):

    if marble % 23 == 0:
        board.rotate(7)

        player_id = marble % players
        out_marble = board.pop()
        scores[player_id] += marble + out_marble

        board.rotate(-1)
    else:
        board.rotate(-1)
        board.append(marble)

    if marble == marbles:
        solution = max(scores.values())

solution2 = max(scores.values())

print(f'P9-1: {solution}')
print(f'P9-2: {solution2}')
