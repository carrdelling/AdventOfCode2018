
class Device:

    def __init__(self):

        self.registers = {0: 0, 1: 0, 2: 0, 3: 0}

        self.operations = {'addr': self.addr,
                           'addi': self.addi,
                           'mulr': self.mulr,
                           'muli': self.muli,
                           'banr': self.banr,
                           'bani': self.bani,
                           'borr': self.borr,
                           'bori': self.bori,
                           'setr': self.setr,
                           'seti': self.seti,
                           'gtir': self.gtir,
                           'gtri': self.gtri,
                           'gtrr': self.gtrr,
                           'eqir': self.eqir,
                           'eqri': self.eqri,
                           'eqrr': self.eqrr}

    def reset(self, a, b, c, d):
        self.registers = {0: a, 1: b, 2: c, 3: d}

    def apply_opname(self, opname, params):
        self.operations[opname](*params)

    def addr(self, a, b, c):
        """ addr (add register) stores into register C the result of adding register A and register B. """

        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a, b, c):
        """ addi (add immediate) stores into register C the result of adding register A and value B. """

        self.registers[c] = self.registers[a] + b

    def mulr(self, a, b, c):
        """ mulr (multiply register) stores into register C the result of multiplying register A and register B. """

        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a, b, c):
        """ muli (multiply immediate) stores into register C the result of multiplying register A and value B. """

        self.registers[c] = self.registers[a] * b

    def banr(self, a, b, c):
        """ banr (bitwise AND register)
            stores into register C the result  of the bitwise AND of register A and register B.
        """

        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a, b, c):
        """ bani (bitwise AND immediate)
            stores into register C the result of the bitwise AND of register A and value B
        """

        self.registers[c] = self.registers[a] & b

    def borr(self, a, b, c):
        """ borr (bitwise OR register)
            stores into register C the result of the bitwise OR of register A and register B.
        """

        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a, b, c):
        """ bori (bitwise OR immediate)
            stores into register C the result of the bitwise OR of register A and value B.
        """

        self.registers[c] = self.registers[a] | b

    def setr(self, a, b, c):
        """ setr (set register) copies the contents of register A into register C. (Input B is ignored.) """
        self.registers[c] = self.registers[a]

    def seti(self, a, b, c):
        """ seti (set immediate) stores value A into register C. (Input B is ignored.) """
        self.registers[c] = a

    def gtir(self, a, b, c):
        """ gtir (greater-than immediate/register)
            sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
        """

        self.registers[c] = 1 if a > self.registers[b] else 0

    def gtri(self, a, b, c):
        """ gtri (greater-than register/immediate)
            sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
        """

        self.registers[c] = 1 if self.registers[a] > b else 0

    def gtrr(self, a, b, c):
        """ gtrr (greater-than register/register)
            sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
        """

        self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0

    def eqir(self, a, b, c):
        """ eqir (equal immediate/register)
            sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
        """

        self.registers[c] = 1 if a == self.registers[b] else 0

    def eqri(self, a, b, c):
        """ eqri (equal register/immediate)
            sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
        """

        self.registers[c] = 1 if self.registers[a] == b else 0

    def eqrr(self, a, b, c):
        """ eqrr (equal register/register)
            sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
        """

        self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0


def solve(cases):

    pc = Device()

    solution = 0
    for before, ins, after in cases:

        valid = 0
        for op_name in pc.operations:
            pc.reset(*before)
            pc.apply_opname(op_name, ins[1:])
            state = tuple(pc.registers[i] for i in range(4))

            if state == after:
                valid += 1

        solution += 1 if valid >= 3 else 0

    return solution


def main():

    with open("input") as in_f:
        cases = []
        buffer = []
        numbers = False
        for row in in_f:
            if len(row) < 1:
                continue

            if 'Before' in row:
                # Before: [1, 2, 2, 1]
                data = tuple(map(int, row.split('[')[-1].split(']')[0].split(', ')))
                buffer.append(data)
                numbers = True
                continue

            if 'After' in row:
                # After: [1, 2, 2, 1]
                data = tuple(map(int, row.split('[')[-1].split(']')[0].split(', ')))
                buffer.append(data)

                cases.append(tuple(buffer))
                buffer = []
                numbers = False
                continue

            if numbers:
                data = tuple(map(int, row.strip().split(' ')))
                buffer.append(data)
                continue

    solution = solve(cases)

    print(solution)


if __name__ == "__main__":

    main()
