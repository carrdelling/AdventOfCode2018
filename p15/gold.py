

def neighbors(i, j):
    return [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]


class Character:

    def __init__(self, i, j, t):
        self.hit_points = 200
        self.attack = 3
        self.x = i
        self.y = j
        self.tag = t

    @property
    def location(self):
        return self.x, self.y

    @property
    def damage(self):
        return self.attack

    @property
    def life(self):
        return self.hit_points

    @property
    def alive(self):
        return self.hit_points > 0

    @property
    def is_elf(self):
        return None

    @property
    def identity(self):
        return self.tag

    def hit(self, damage):
        self.hit_points -= damage
        self.hit_points = max(self.hit_points, 0)

    def move(self, i, j):
        self.x = i
        self.y = j


class Elf(Character):

    @property
    def is_elf(self):
        return True

    def __repr__(self):
        if self.alive:
            return f"Elf {self.tag}: HP={self.life}; Pos={self.location}"
        return f"{self.tag}: DEAD"


class Goblin(Character):

    @property
    def is_elf(self):
        return False

    def __repr__(self):
        if self.alive:
            return f"Goblin {self.tag}: HP={self.life}; Pos={self.location}"
        return f"{self.tag}: DEAD"


class Battle:

    def __init__(self, data, elf_power=3):

        self.scenario = {}
        self.max_x = len(data)
        self.max_y = len(data[0])

        self.rounds = 0

        self.elves = {}
        self.goblins = {}

        for i, row in enumerate(data):
            for j, c in enumerate(row):
                self.scenario[(i, j)] = c

                if c == 'G':
                    self._create_goblin(i, j)

                if c == 'E':
                    self._create_elf(i, j, elf_power)

    def _create_elf(self, i, j, power):
        tag = len(self.elves)

        new_elf = Elf(i, j, tag)
        new_elf.attack = power
        self.elves[tag] = new_elf

    def _create_goblin(self, i, j):
        tag = len(self.goblins)

        new_goblin = Goblin(i, j, tag)
        self.goblins[tag] = new_goblin

    def _action(self, side, n):

        # cancel action if it died in this turn
        is_alive = self.elves[n].alive if side else self.goblins[n].alive
        if not is_alive:
            return 0

        targets = self._find_targets(side)

        # combat ends
        if not targets:
            return -1

        current_position = self.elves[n].location if side else self.goblins[n].location
        target = self._find_route(targets, current_position)

        # turn ends because there are no reachable targets
        if target is None:
            return 0

        # move: define & apply the movement
        if target != current_position:
            movement = self._find_movement(target, current_position)
            self.scenario[current_position] = '.'

            if side:
                self.scenario[movement] = 'E'
                self.elves[n].move(*movement)
            else:
                self.scenario[movement] = 'G'
                self.goblins[n].move(*movement)
            current_position = movement

        # attack: find enemies alive
        atk_range = {n for n in neighbors(*current_position)}
        targets = [c for c in (self.elves.values() if not side else self.goblins.values())
                   if c.alive and c.location in atk_range]
        targets.sort(key=lambda x: (x.life, x.location))

        if targets:
            target = targets[0]
            nt = target.tag
            if side:
                self.goblins[nt].hit(self.elves[n].attack)

                if not self.goblins[nt].alive:
                    self.scenario[self.goblins[nt].location] = '.'
                    self.goblins[nt].move(-1, -1)
            else:
                self.elves[nt].hit(self.goblins[n].attack)

                if not self.elves[nt].alive:
                    self.scenario[self.elves[nt].location] = '.'
                    self.elves[nt].move(-1, -1)

        # turn ends!

    def _find_targets(self, side):
        return [c for c in (self.elves.values() if not side else self.goblins.values()) if c.alive]

    def _find_route(self, enemies, current_position):

        targets = {n for e in enemies for n in neighbors(*e.location)}

        return self._reachability(targets, current_position)

    def _reachability(self, targets, current):

        reached = {current}
        changed = True

        while changed:
            changed = False

            in_range = targets & reached

            if in_range:
                return sorted(in_range)[0]

            for r in list(reached):
                for n in (x for x in neighbors(*r) if x not in reached):
                    if self.scenario.get((n[0], n[1]), '#') == '.':
                        reached.add(n)
                        changed = True

        return None

    def _find_movement(self, target, current_position):

        posibilities = {n for n in neighbors(*current_position)}
        reached = {target}

        while True:

            in_range = posibilities & reached

            if in_range:
                return sorted(in_range)[0]

            for r in list(reached):
                for n in (x for x in neighbors(*r) if x not in reached):
                    if self.scenario.get((n[0], n[1]), '#') == '.':
                        reached.add(n)

    @property
    def score(self):
        return self.rounds * (sum(g.life for g in self.goblins.values()) +
                              sum(e.life for e in self.elves.values())
                              )

    @property
    def all_elves_alive(self):
        return all(e.alive for e in self.elves.values())

    def show(self):

        print("*" * 30)
        print(f"Round {self.rounds}")
        print(f"Score {self.score}")
        print("*" * 30)
        for i in range(self.max_x):
            row = []
            for j in range(self.max_y):
                row.append(self.scenario[(i, j)])
            print(''.join(row))
        print("=" * 30)
        print(f"{len(self.elves)} elves")
        for k in sorted(self.elves):
            print(self.elves[k])
        print("=" * 30)
        print(f"{len(self.goblins)} goblins")
        for k in sorted(self.goblins):
            print(self.goblins[k])

    def round(self):

        # compute turns
        turns = [(e.location, True, t) for t, e in self.elves.items() if e.alive]
        turns += [(g.location, False, t) for t, g in self.goblins.items() if g.alive]
        turns.sort()

        for _, side, tag in turns:
            result = self._action(side, tag)

            if result == -1:
                return False

        self.rounds += 1
        return True


def solve(data):

    for power in range(4, 200):
        game = Battle(data, elf_power=power)

        while game.round():
            pass

        if game.all_elves_alive:
            game.show()
            print(power)
            return game.score

    return None


def main():

    with open("input") as in_f:
        scenario = []
        for row in in_f:
            scenario.append([c for c in row.strip()])

    solution = solve(scenario)

    print(solution)


if __name__ == "__main__":

    main()
