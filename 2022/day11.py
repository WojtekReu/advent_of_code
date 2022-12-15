#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/11
"""
from typing import Self

ROUNDS_RANGE_1 = 20
ROUNDS_RANGE_2 = 10_000


def read_input():
    with open('day11_input.txt', "r") as f:
    # with open('test.txt', "r") as f:
        data = f.read()

    items_count = 0
    monkeys = []
    monkey = None

    for line in data.split("\n"):
        # print(line)
        words = line.lstrip().split()
        if not len(words):
            continue
        elif words[0] == 'Monkey':
            monkey = Monkey(words[1])
            monkeys.append(monkey)
        elif words[0] == 'Starting':
            for nr_str in words[2:]:
                item = Item(items_count, nr_str)
                items_count += 1
                monkey.append(item)
        elif words[0].startswith('Operation'):
            monkey.set_operation(words[4], words[5])
        elif words[0].startswith('Test:'):
            monkey.set_divisible_by(words[-1])
        elif words[0].startswith('If'):
            monkey.set_destinations_nr(words[1], words[5])
    return monkeys


def set_destinations(monkeys):
    for monkey in monkeys:
        monkey.set_destinations(monkeys)


def draw(monkeys):
    output = ""
    for monkey in monkeys:
        output += f"{monkey}  --> {monkey.items}\n"
    return output


def throw_items(monkeys, rounds_range, lcm=None, are_bored=True):
    for m_round in range(rounds_range):
        for monkey in monkeys:
            for item in monkey.items:
                item.worry_level = monkey.operation(item.worry_level)
                if are_bored:
                    item.get_bored()
                result = monkey.test(item)
                if lcm:
                    item.worry_level = item.worry_level % lcm
                if result:
                    monkey.true_destination.append(item)
                else:
                    monkey.false_destination.append(item)
            monkey.items = []


def get_least_common_multiple(monkeys):
    lcm = 1
    for monkey in monkeys:
        lcm *= monkey.divisible_by
    return lcm


def inspect_monkeys(monkeys):
    for monkey in monkeys:
        print(f"Monkey {monkey.nr} inspected items {monkey.activity_count} times.")
    activiti_list = sorted([m.activity_count for m in monkeys])
    # print(activiti_list)
    return activiti_list[-2] * activiti_list[-1]


class Item:
    worry_level: int

    def __init__(self, nr, worry_level):
        self.item_nr = int(nr)
        self.worry_level = int(worry_level.strip(','))

    def __repr__(self):
        return f"<{self.item_nr}_{self.worry_level}>"

    def get_bored(self):
        self.worry_level = int(self.worry_level / 3)


class Monkey:
    true_destination: Self
    false_destination: Self
    true_destination_nr: int
    false_destination_nr: int
    operation_value: int | None
    operation_function: str  # + *
    divisible_by: int
    activity_count = 0

    def __init__(self, nr_str: str):
        self.nr = int(nr_str.rstrip(':'))
        self.items = []

    def __repr__(self):
        return f"Monkey {self.nr}, {self.operation_function} {self.operation_value} {self.divisible_by}"

    def operation(self, worry_level: int) -> int:
        value = self.operation_value or worry_level
        if self.operation_function == '+':
            return worry_level.__add__(value)
        elif self.operation_function == '*':
            return worry_level.__mul__(value)

    def is_divisible(self, worry_level):
        if worry_level % self.divisible_by == 0:
            return True
        return False

    def test(self, item: Item):
        self.activity_count += 1
        result = self.is_divisible(item.worry_level)
        return result

    def append(self, item: Item):
        self.items.append(item)

    def set_destinations(self, monkeys):
        self.true_destination = monkeys[self.true_destination_nr]
        self.false_destination = monkeys[self.false_destination_nr]

    def set_destinations_nr(self, bool_word: str, monkey_nr_word: str):
        monkey_nr = int(monkey_nr_word)
        if bool_word == 'true:':
            self.true_destination_nr = monkey_nr
        elif bool_word == 'false:':
            self.false_destination_nr = monkey_nr

    def set_operation(self, operation, value):
        self.operation_function = operation
        try:
            number_or_none = int(value)
        except ValueError:
            number_or_none = None
        self.operation_value = number_or_none

    def set_divisible_by(self, value):
        self.divisible_by = int(value)


monkeys_data = read_input()
set_destinations(monkeys_data)
pic = draw(monkeys_data)
print(pic)

throw_items(monkeys_data, ROUNDS_RANGE_1)
monkey_business = inspect_monkeys(monkeys_data)
print(f"The level of monkey business after {ROUNDS_RANGE_1} rounds is {monkey_business}")

least_common_multiple = get_least_common_multiple(monkeys_data)
print(f"Least common multiple for all 'divisible_by' numbers is {least_common_multiple=}.")

throw_items(monkeys_data, ROUNDS_RANGE_2, lcm=least_common_multiple, are_bored=False)
monkey_business = inspect_monkeys(monkeys_data)
print(f"The level of monkey business after {ROUNDS_RANGE_2} rounds is {monkey_business}")
