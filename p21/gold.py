

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


def search_value(program):

    pc = Device()
    pc.registers[0] = 1   # will loop forever

    # process the ip instruction first
    pc.set_ip(program[0][-1])
    program = program[1:]

    exit_values = set()
    last_exit = -1
    while 0 <= pc.ip < len(program):
        op = program[pc.ip]

        pc.apply_opname(op[0], op[1:])
        pc.inc_ip()

        # the exit is here
        if pc.ip == 28:
            exit_val = pc.registers[2]
            if exit_val in exit_values or len(exit_values) > 5:
                print(exit_values)
                break
            else:
                last_exit = exit_val
                exit_values.add(exit_val)
                print(len(exit_values))

    return last_exit

"""

My input program:

#ip 1
0: seti 123 0 2    ==>     L1: R2 = 123
1: bani 2 456 2                R2 = R2 & 456
2: eqri 2 72 2                 R2 == 72 ? --> R2=1, R2=0  (1= Jump L2)
3: addr 2 1 1                  R1 = R1 + R2
4: seti 0 0 1                  R1 = 0  --> Jump L1
5: seti 0 3 2              L2: R2 = 0
6: bori 2 65536 5          L6: R5 = R2 | 65536 
7: seti 4843319 1 2            R2 = 4843319
8: bani 5 255 4           L11: R4 = R5 & 255
9: addr 2 4 2                  R2 = R2 + R4
10: bani 2 16777215 2          R2 = R2 & 16777215
11: muli 2 65899 2             R2 = R2 * 65899
12: bani 2 16777215 2          R2 = R2 & 16777215
13: gtir 256 5 4               R4 = 1 if 256 > R5 else 0  (1= Jump L3/L5, 0= Jump L4)
14: addr 4 1 1                 R1 = R4 + R1
15: addi 1 1 1                 R1 = R1 + R1  (Jump to L4)
16: seti 27 4 1            L3: R1 = 27   (Jump to L5)
17: seti 0 7 4             L4: R4 = 0
18: addi 4 1 3            L10: R3 = R4 + 1
19: muli 3 256 3               R3 = R3 * 256
20: gtrr 3 5 3                 R3 = 1 if R3 > R5 else 0   (1= Jump L7/L8, 0= Jump L9)
21: addr 3 1 1                 R1 = R3 + R1
22: addi 1 1 1                 R1 = R1 + R1  (Jump to L9)
23: seti 25 0 1            L7: R1 = 25   (Jump to L8)
24: addi 4 1 4             L9: R4 = R4 + 1
25: seti 17 0 1                R1 = 17   (Jump to L10)
26: setr 4 1 5             L8: R5 = R4
27: seti 7 3 1                 R1 = 7    (Jump to L11)
28: eqrr 2 0 4             L5: R4 = 1 if R0 == R2 else 0  (1= halt, 0= jump L6)
29: addr 4 1 1                 R1 = R1 + R4
30: seti 5 3 1                 R1 = 5

Step 1:

6: bori 2 65536 5          L6: R5 = R2 | 65536 
7: seti 4843319 1 2            R2 = 4843319
8: bani 5 255 4           L11: R4 = R5 & 255
10: bani 2 16777215 2          R2 = (R2 + R4) & 16777215
12: bani 2 16777215 2          R2 = (R2 * 65899) & 16777215
13: gtir 256 5 4               if 256 > R5:
                                     if R0 == R2 WIN!
                                     else jump L6
                               R4 = 0
18: addi 4 1 3            L10: R3 = R4 + 1
19: muli 3 256 3               R3 = R3 * 256
20: gtrr 3 5 3                 if R3 > R5:
                                    R5 = R4 
                                    (Jump to L11)
                               else 
                                    R4 += 1
                                    (Jump to L10)

Solution: Exit the first time R0 == R2, in `28: eqrr 2 0 4` 

Solution 2: When R2 values start repeating on that test, it will never halt anymore
            Just return the last unique R2 number seen
            
            However, by simulation it might take hours!
            
            The first candidates (computed by simulation) are these:
            {8797248, 3928610, 9987174, 6703784, 9317588, 14987870}

            With this, we can write the math routine instead:
            
        R5 = R2 | 65536
        R2 = 4843319

        while True:
            R2 = (((R2 + (R5 & 255)) & 16777215) * 65899) & 16777215

            if R5 < 256:
                solutions.add(R2)
                break

            R5 = R5 // 256
            
            And just wait until we get the last number that isn't repeated


"""


def routine():

    # set up
    solutions = set()
    R2 = 0
    last_found = 0
    changing = True

    while changing:

        R5 = R2 | 65536
        R2 = 4843319

        while True:
            R2 = (((R2 + (R5 & 255)) & 16777215) * 65899) & 16777215

            if R5 < 256:
                changing = R2 not in solutions
                if changing:
                    last_found = R2
                    solutions.add(R2)
                break

            R5 = R5 // 256

    return last_found


def solve(program):

    # naive solution (can get a few values - too slow for all!)
    # solution = search_value(program)

    # convert into a math routine
    solution = routine()

    return solution


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
