#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/24
pypy3 real time  0m0,822s
"""
from tools.input import read_input

FILENAME_INPUT = "day24.input.txt"


class Instruction:
    next = None

    def __init__(self, instruction_name, a, b=None):
        self.instruction = getattr(self, instruction_name)
        self.a = a
        if b is not None:
            try:
                self.b = int(b)
            except ValueError:
                self.b = b

    def __repr__(self):
        return f"{self.instruction.__name__} {self.a} {self.b if hasattr(self, 'b') else ''}"

    @staticmethod
    def inp(a):
        return int(a)

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def mul(a, b):
        return a * b

    @staticmethod
    def div(a, b):
        return a // b

    @staticmethod
    def mod(a, b):
        return a % b

    @staticmethod
    def eql(a, b):
        return 1 if a == b else 0

    def go_inst(self, alu):
        a = alu[self.a]
        b = alu[self.b] if isinstance(self.b, str) else self.b
        alu[self.a] = self.instruction(a, b)  # instructions without the first instruction.
        if self.next:
            self.next.go_inst(alu)

    def calc(self, z: int, value: int) -> int:
        alu = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": z,
        }
        # Only the first instruction always is `inp` with one argument `value`.
        alu[self.a] = self.instruction(value)  # this replaces one of the above values in alu.
        if self.next:
            self.next.go_inst(alu)
        return alu["z"]


def prepare(data):
    instructions = []
    inst_before = None
    for line in data.split("\n"):
        words = line.split()
        if len(words) < 3:
            inst = Instruction(words[0], words[1])
            instructions.append(inst)
            inst_before = None
        else:
            inst = Instruction(words[0], words[1], words[2])
        if inst_before:
            inst_before.next = inst
        inst_before = inst

    return instructions


def get_d_min(z2, state_new, d_min_previous, d):
    if z2 in state_new and state_new[z2][0] < d_min_previous:
        return state_new[z2][0]
    return f"{d_min_previous}{d}"


def calculate(instructions):
    state = {0: ("", "")}
    borders = []  # lifo - borders for `i`
    half = len(instructions) // 2  # 14 // 2 = 7

    for i in range(half):  # the first half instructions
        inst = instructions[i]
        state_new = {}

        for z1, (d_min, d_max) in state.items():
            for d in range(1, 10):
                z2 = inst.calc(z1, d)
                state_new[z2] = get_d_min(z2, state_new, d_min, d), f"{d_max}{d}"
        state = state_new
        borders.append(max(abs(min(state)), abs(max(state))))
        # print(i, len(state))

    for i in range(half, len(instructions)):  # the last half instructions
        inst = instructions[i]
        state_new = {}
        z2_max = borders.pop()
        z2_min = -z2_max

        for z1, (d_min, d_max) in state.items():
            for d in range(1, 10):
                z2 = inst.calc(z1, d)
                if z2_min <= z2 < z2_max:  # add only when z is in range specific for `i`
                    state_new[z2] = get_d_min(z2, state_new, d_min, d), f"{d_max}{d}"
        state = state_new
        # print(i, len(state))
    return state[0]


def main(filename):
    data = read_input(filename)
    instr = prepare(data)
    smallest, largest = calculate(instr)
    print(f"The largest model number accepted by MONAD is {largest}.")
    print(f"The smallest model number accepted by MONAD is {smallest}.")
    assert largest == "94399898949959"
    assert smallest == "21176121611511"


if __name__ == "__main__":
    main(FILENAME_INPUT)
