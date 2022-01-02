

class Unit:

    def __init__(self, data):

        self.units = int(data.split()[0])
        self.hp = int(data.split()[4])
        self.ini = int(data.split()[-1])

        self.target = -1

        # attack
        damage, attack = data.split(' attack that does ')[-1].split(' damage')[0].split()
        self.damage = int(damage)
        self.attack = attack

        # defense
        self.weak = set()
        self.inmune = set()

        if '(' not in data:
            return
        text = data.split('(')[-1].split(')')[0]

        if ';' in text:
            parts = [p.strip() for p in text.split(';')]
        else:
            parts = [text.strip()]

        for p in parts:
            _type, names = p.split(' to ')
            is_weak = _type == 'weak'
            names = {x for x in names.split(', ')}

            if is_weak:
                self.weak |= names
            else:
                self.inmune |= names

    def __repr__(self):
        msg = f"{self.units} ({self.hp}) A: {self.damage} ({self.attack}) D: {self.inmune}/{self.weak} =>"
        msg += f"I: {self.ini} T: {self.target}"
        return msg

    @property
    def is_alive(self):
        return self.units > 0

    @property
    def effective_power(self):
        return self.units * self.damage

    def get_damage(self, points, kind):

        if kind in self.inmune:
            damage = 0
        elif kind in self.weak:
            damage = points * 2
        else:
            damage = points

        loses = damage // self.hp

        self.units = max(0, self.units - loses)


def target_phase(body_army, infection_army):

    # targeting - body army
    power_ini = [(idx, body_army[idx].effective_power, body_army[idx].ini) for idx in body_army]
    power_ini.sort(key=lambda x: (-x[1], -x[1]))

    targeted = set()
    for idx, _, _ in power_ini:
        a_type = body_army[idx].attack

        # try weak enemies
        weak_e = [(i, infection_army[i].effective_power, infection_army[i].ini)
                  for i in infection_army if (a_type in infection_army[i].weak)
                  and infection_army[i].is_alive and i not in targeted]

        weak_e.sort(key=lambda x: (-x[1], -x[2]))

        normal_e = []
        if not weak_e:
            # try normal enemies
            normal_e = [(i, infection_army[i].effective_power, infection_army[i].ini)
                        for i in infection_army if (a_type not in infection_army[i].inmune) and
                        infection_army[i].is_alive and i not in targeted]
            normal_e.sort(key=lambda x: (-x[1], -x[2]))

        target = weak_e[0][0] if weak_e else (normal_e[0][0] if normal_e else -1)
        target = -1 if not body_army[idx].is_alive else target
        body_army[idx].target = target

        targeted.add(target)

    # targeting - infection army
    power_ini = [(idx, infection_army[idx].effective_power, infection_army[idx].ini) for idx in infection_army]
    power_ini.sort(key=lambda x: (-x[1], -x[1]))

    targeted = set()
    for idx, _, _ in power_ini:
        a_type = infection_army[idx].attack

        # try weak enemies
        weak_e = [(i, body_army[i].effective_power, body_army[i].ini)
                  for i in body_army if (a_type in body_army[i].weak) and
                  body_army[i].is_alive and i not in targeted]
        weak_e.sort(key=lambda x: (-x[1], -x[2]))

        normal_e = []
        if not weak_e:
            # try normal enemies
            normal_e = [(i, body_army[i].effective_power, body_army[i].ini)
                        for i in body_army if (a_type not in body_army[i].inmune) and
                        body_army[i].is_alive and i not in targeted]
            normal_e.sort(key=lambda x: (-x[1], -x[2]))

        target = weak_e[0][0] if weak_e else (normal_e[0][0] if normal_e else -1)
        target = -1 if not infection_army[idx].is_alive else target
        infection_army[idx].target = target

        targeted.add(target)


def solve(body, infection):

    body_army = {idx: Unit(x) for idx, x in enumerate(body)}
    infection_army = {idx: Unit(x) for idx, x in enumerate(infection)}

    # initiative - does not change for the whole fight
    initiative = [('body', idx, body_army[idx].ini) for idx in body_army]
    initiative += [('infection', idx, infection_army[idx].ini) for idx in infection_army]
    initiative.sort(key=lambda x: -x[2])

    stalemate = False

    while body_army and infection_army and (not stalemate):

        # targeting
        target_phase(body_army, infection_army)

        # attacking
        stalemate = True
        for team, idx, _ in initiative:
            is_body = team == 'body'

            attacker = body_army[idx] if is_body else infection_army[idx]
            target_id = attacker.target
            if (not attacker.is_alive) or (target_id == -1):
                continue

            defender = infection_army[target_id] if is_body else body_army[target_id]

            if not defender.is_alive:
                continue

            # attack happens
            stalemate = False
            defender.get_damage(attacker.effective_power, attacker.attack)

    print('body status')
    print('===========')
    for u in body_army:
        unit = body_army[u]
        if unit.is_alive:
            print(u, unit)

    print('infection status')
    print('===========')
    for u in infection_army:
        unit = infection_army[u]
        if unit.is_alive:
            print(u, unit)

    solution = sum(u.units for u in body_army.values())
    solution += sum(u.units for u in infection_army.values())

    return solution


def main():

    body = []
    infection = []
    with open("input") as in_f:
        infection_army = False
        for row in in_f:
            if len(row) < 2:
                continue

            if "Infection" in row:
                infection_army = True

            if "units" in row:
                if infection_army:
                    infection.append(row.strip())
                else:
                    body.append(row.strip())

    solution = solve(body, infection)

    print(solution)


if __name__ == "__main__":

    main()
