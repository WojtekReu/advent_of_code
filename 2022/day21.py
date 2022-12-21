#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/21
"""
from typing import Self


def read_input() -> dict:
    with open('day21.input.txt', "r") as f:
    # with open('day21.test.txt', "r") as f:
        data = f.read()

    monkeys: dict[str, Monkey] = {}
    for line in data.split("\n"):
        words = line.split()
        name = words[0].rstrip(":")
        if name in monkeys.keys():
            raise ValueError(f'Error: {name} monkey exist in dict')
        if len(words) < 3:
            monkeys[name] = Monkey(name, number=int(words[1]))
        else:
            monkeys[name] = Monkey(name, operation=words[2])
            monkeys[name].left_monkey = words[1]
            monkeys[name].right_monkey = words[3]
    return monkeys


class Monkey:
    name: str
    left_monkey: str
    right_monkey: str
    operation: str
    number: int

    def __init__(self, name, operation=None, number=None):
        self.name = name
        self.operation = operation
        self.number = number

    def __repr__(self):
        if self.number:
            return f"<{self.name}: {self.number}>"
        return f"<{self.name}: {self.left_monkey} {self.operation} {self.right_monkey}>"

    def calculate(self, monkeys):
        if self.number:
            return self.number
        else:
            left_monkey = monkeys[self.left_monkey]
            right_monkey = monkeys[self.right_monkey]
            if self.operation == '+':
                return left_monkey.calculate(monkeys) + right_monkey.calculate(monkeys)
            elif self.operation == '-':
                return left_monkey.calculate(monkeys) - right_monkey.calculate(monkeys)
            elif self.operation == '*':
                return left_monkey.calculate(monkeys) * right_monkey.calculate(monkeys)
            elif self.operation == '/':
                return left_monkey.calculate(monkeys) / right_monkey.calculate(monkeys)
            else:
                raise ValueError("Operation not found.")


def find_root(monkeys):
    root = monkeys['root']
    result = root.calculate(monkeys)
    return result


monkeys_data = read_input()

# print(monkeys_data)
result = find_root(monkeys_data)

print(f"result is {result}.")

