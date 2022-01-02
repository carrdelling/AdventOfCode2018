

class Device:

    def __init__(self):

        self._ip = 0

        self.registers = {0: 0, 1: 0, 2: 0,
                          3: 0, 4: 0, 5: 0
                          }

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

        self.num_operations = {}

    def reset(self, a, b, c, d, e, f, ip):
        self.registers = {0: a, 1: b, 2: c, 3: d, 4: e, 5: f}
        self._ip = ip

    def set_ip(self, ip):
        self._ip = ip

    def inc_ip(self):
        self.registers[self._ip] += 1

    @property
    def ip(self):
        return self.registers[self._ip]

    def install_ops(self, mappings):

        for k, code in mappings.items():
            self.num_operations[k] = self.operations[next(iter(code))]

    def apply_opname(self, opname, params):
        self.operations[opname](*params)

    def apply_op(self, op, params):
        self.num_operations[op](*params)

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


def solve(program):

    pc = Device()

    # process the ip instruction first
    pc.set_ip(program[0][-1])
    program = program[1:]

    while 0 <= pc.ip < len(program):
        op = program[pc.ip]
        pc.apply_opname(op[0], op[1:])
        pc.inc_ip()

    return pc.registers[0]


def main():

    with open("input") as in_f:
        program = []
        for row in in_f:
            if len(row) < 2:
                continue

            if '#ip' in row:
                v = int(row.strip().split()[-1])
                ins = ('#ip', v)
            else:
                ins = list(row.strip().split())
                for i in range(1, len(ins)):
                    ins[i] = int(ins[i])
            program.append(ins)

    solution = solve(program)

    print(solution)


if __name__ == "__main__":

    main()
