#!/usr/bin/env python3
"""
https://adventofcode.com/2015/day/7
real time  0m0,024s
"""
from tools.input import read_input

FILENAME_INPUT = "day07.input.txt"
FILENAME_TEST = "day07.test.txt"


class Gate:
    result: int = None
    max = 65535  # signal has 16-bit (a number from 0 to 65535)

    def __init__(self, name: str, operation: str, inputs: list):
        self.name = name  # lower chars string
        self.operation = operation  # upper chars string or empty string
        self.a = inputs[0]  # lower chars string or int
        self.b = inputs[1] if 1 < len(inputs) else None  # lower chars string or int or None

    def __repr__(self):
        return f"{self.a} {self.operation} {self.b or ''} -> {self.name}"

    def calculate(self, gates):
        if self.result is None:
            a = gates[self.a].calculate(gates) if isinstance(self.a, str) else self.a
            b = gates[self.b].calculate(gates) if isinstance(self.b, str) else self.b
            self.result = self.do(a, b)
            # print(f"{a} {self.operation} {b} -> {self.result}")
        return self.result

    def do(self, a, b) -> int:
        if self.operation == "":
            return a
        elif self.operation == "AND":
            return a & b
        elif self.operation == "OR":
            return a | b
        elif self.operation == "LSHIFT":
            return a << b & self.max
        elif self.operation == "RSHIFT":
            return a >> b
        elif self.operation == "NOT":
            return ~a & self.max


def prepare(data):
    gates = {}
    for line in data.split("\n"):
        inputs = []
        operation = ""
        create_gate = False
        for word in line.split():
            if create_gate:
                gates[word] = Gate(word, operation, inputs)  # always last word in line
            elif word == "->":
                create_gate = True  # always one before last word in line
            elif word.isupper():
                operation = word
            elif word.islower():
                inputs.append(word)
            else:
                inputs.append(int(word))

    return gates


def calculate(gates) -> int:
    # for name, gate in gates.items():
    #     print(name, ": ", gate)

    gate_a = gates["a"]  # for tests use 'i'
    result = gate_a.calculate(gates)
    return result


def calculate2(gates, result_a):
    for gate in gates.values():
        gate.result = None  # reset

    gates["b"].result = result_a
    result = gates["a"].calculate(gates)
    return result


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    g = prepare(data)
    result1 = calculate(g)
    print(f"Signal {result1} is ultimately provided to wire a.")

    result2 = calculate2(g, result1)
    print(f"After overriding b to result from a, new signal {result2} is provided to wire a.")

    assert result1 == 3176
    assert result2 == 14710
