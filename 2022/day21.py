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
            monkeys[name].left_name = words[1]
            monkeys[name].right_name = words[3]
    return monkeys


class ReverseOperation:
    left: int | Self
    right: int | Self
    operator: str
    reversed_operator: str

    def __init__(self, left=0, operator_str='', right=0):
        self.left = left
        self.operator = operator_str
        self.right = right
        self.set_reversed_operator()

    def __repr__(self):
        if isinstance(self.left, ReverseOperation):
            return f"unknown {self.reversed_operator} {self.right}"
        if isinstance(self.right, ReverseOperation):
            return f"{self.left} {self.reversed_operator} unknown"
        return f"{self.left} {self.reversed_operator} {self.right}"

    def set_reversed_operator(self):
        match self.operator:
            case '+':
                self.reversed_operator = '-'
            case '-':
                self.reversed_operator = '+'
            case '*':
                self.reversed_operator = '/'
            case '/':
                self.reversed_operator = '*'
            case _:
                self.reversed_operator = '?'

    def reverse_calculation(self, missing_side):
        if self.operator == '':
            return missing_side

        if self.operator == '+':
            if isinstance(self.left, ReverseOperation):
                return self.left.reverse_calculation(missing_side - self.right)
            else:
                return self.right.reverse_calculation(missing_side - self.left)
        if self.operator == '-':
            if isinstance(self.left, ReverseOperation):
                return self.left.reverse_calculation(missing_side + self.right)
            else:
                return self.right.reverse_calculation(-missing_side + self.left)
        if self.operator == '*':
            if isinstance(self.left, ReverseOperation):
                value = missing_side / self.right
                return self.left.reverse_calculation(value)
            else:
                value = missing_side / self.left
                return self.right.reverse_calculation(value)
        if self.operator == '/':
            if isinstance(self.left, ReverseOperation):
                return self.left.reverse_calculation(missing_side * self.right)
            else:
                return self.right.reverse_calculation(self.left / missing_side)


class Monkey:
    name: str
    left_name: str
    right_name: str
    operation: str
    number: int

    def __init__(self, name, operation=None, number=None):
        self.name = name
        self.operation = operation
        self.number = number

    def __repr__(self):
        if self.number:
            return f"<{self.name}: {self.number}>"
        return f"<{self.name}: {self.left_name} {self.operation} {self.right_name}>"

    def calculate(self, monkeys):
        if self.number is not None:
            return self.number
        else:
            left_monkey = monkeys[self.left_name]
            right_monkey = monkeys[self.right_name]
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

    def find_or_calculate(self, monkeys, monkey_name) -> Self | int:
        if self.name == monkey_name:
            return ReverseOperation()
        if hasattr(self, 'left_name'):
            left_monkey = monkeys[self.left_name]
            right_monkey = monkeys[self.right_name]

            left_side = left_monkey.find_or_calculate(monkeys, monkey_name)
            right_side = right_monkey.find_or_calculate(monkeys, monkey_name)
            if left_side and isinstance(left_side, ReverseOperation):
                return ReverseOperation(left_side, self.operation, right_side)

            if right_side and isinstance(right_side, ReverseOperation):
                return ReverseOperation(left_side, self.operation, right_side)

        return self.calculate(monkeys)

    def predict_humn_number(self, monkeys, monkey_name):
        left_monkey = monkeys[self.left_name]
        right_monkey = monkeys[self.right_name]
        left_side = left_monkey.find_or_calculate(monkeys, monkey_name)
        right_side = right_monkey.find_or_calculate(monkeys, monkey_name)

        if isinstance(left_side, ReverseOperation):
            searched_value = left_side.reverse_calculation(right_side)
        elif isinstance(right_side, ReverseOperation):
            searched_value = right_side.reverse_calculation(left_side)

        return searched_value


def find_values(monkeys):
    root = monkeys['root']
    monkey_name = 'humn'
    root_result = root.calculate(monkeys)
    humn_result = root.predict_humn_number(monkeys, monkey_name)
    return int(root_result), int(humn_result)


monkeys_data = read_input()

# print(monkeys_data)
result1, result2 = find_values(monkeys_data)

print(f"Root yell {result1} and you should yell {result2}.")
