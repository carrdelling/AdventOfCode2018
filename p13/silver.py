

class Cart:

    def __init__(self, i, j, o, t):

        self.x = i
        self.y = j

        self.orient = o
        self.intersections = 0

        self.tag = t

    def __str__(self):
        return self.tag

    @property
    def location(self):
        return self.x, self.y

    def direction(self, current):

        if current == '|':
            return (-1, 0) if self.orient == '^' else (1, 0)
        if current == '-':
            return (0, -1) if self.orient == '<' else (0, 1)
        if current == '/':
            return {
                '<': (1, 0),
                '>': (-1, 0),
                '^': (0, 1),
                'v': (0, -1),
            }[self.orient]
        if current == '\\':
            return {
                '<': (-1, 0),
                '>': (1, 0),
                '^': (0, -1),
                'v': (0, 1),
            }[self.orient]
        if current == '+':
            if self.intersections == 0:
                direction = {
                    '<': (1, 0),
                    '>': (-1, 0),
                    '^': (0, -1),
                    'v': (0, 1),
                }[self.orient]
            elif self.intersections == 1:
                direction = {
                    '<': (0, -1),
                    '>': (0, 1),
                    '^': (-1, 0),
                    'v': (1, 0),
                }[self.orient]
            elif self.intersections == 2:
                direction = {
                    '<': (-1, 0),
                    '>': (1, 0),
                    '^': (0, 1),
                    'v': (0, -1),
                }[self.orient]
            else:
                assert False

            self.intersections = (self.intersections + 1) % 3

            return direction

    def step(self, track):

        dx, dy = self.direction(track)
        self.x += dx
        self.y += dy

        self.orient = {
            (-1, 0): '^',
            (1, 0): 'v',
            (0, -1): '<',
            (0, 1): '>',
        }[(dx, dy)]

        return self.location


def sim(tracks, carts):

    # collisions checking
    locations = {cart.location for cart in carts}

    for cart in sorted(carts, key=lambda c: c.location):
        old_l = cart.location
        current = tracks[old_l]
        new_l = cart.step(current)

        # collision?
        if new_l in locations:
            return new_l
        locations.remove(old_l)
        locations.add(new_l)

    return None


def solve(tracks):

    # create the carts
    carts = []
    next_tag = ord('A')
    for (i, j), v in tracks.items():

        if v in {'v', '<', '>', '^'}:
            new_cart = Cart(i, j, v, chr(next_tag))

            next_tag += 1
            carts.append(new_cart)

            # clean the track below
            if v in {'<', '>'}:
                tracks[(i, j)] = '-'
            else:
                tracks[(i, j)] = '|'

    # race time!
    clash = None
    while clash is None:
        clash = sim(tracks, carts)

    # for some reason, y and x are reversed in the website solution

    return clash[1], clash[0]


def main():

    with open("input") as in_f:
        data = {}

        for i, row in enumerate(in_f):
            for j, c in enumerate(row):
                if c != '\n':
                    data[(i, j)] = c

    solution = solve(data)

    print(solution)


if __name__ == "__main__":

    main()
