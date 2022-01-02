

def solve(data):

    stack = []
    step = {
        'W': (0, -1),
        'E': (0, 1),
        'N': (-1, 0),
        'S': (1, 0),
    }

    current = (0, 0)
    steps = 0
    max_steps = 0
    shortest_path = {}

    for c in data:
        if c in {'$', '^'}:
            continue

        if c in step:
            s = step[c]
            current = (current[0] + s[0], current[1] + s[1])
            steps += 1

            shortest_path[current] = min(steps, shortest_path.get(current, 999_999_999))
            steps = shortest_path[current]

        if c == '(':
            stack.append((current, steps))
        if c == ')':
            current, steps = stack.pop()
            steps = shortest_path[current]
        if c == '|':
            current, steps = stack[-1]
            steps = shortest_path[current]

        max_steps = max(max_steps, steps)

    return max_steps


def main():

    with open("input") as in_f:
        data = in_f.readline().strip()

    solution = solve(data)

    print(solution)


if __name__ == "__main__":

    main()
