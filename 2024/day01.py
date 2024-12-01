#!/usr/bin/env python3
"""
https://adventofcode.com/2024/day/1
"""
from tools.input import read_input

# FILENAME_INPUT = "day01.test.txt"
FILENAME_INPUT = "day01.input.txt"


def prepare_lists(data):
    list_1 = []
    list_2 = []
    for line in data.split("\n"):
        value_1 = value_2 = None
        for value in line.split(' '):
            if not value:
                continue
            if value_1:
                value_2 = int(value)
            else:
                value_1 = int(value)
        list_1.append(value_1)
        list_2.append(value_2)

    list_1.sort(reverse=True)
    list_2.sort(reverse=True)

    return list_1, list_2

def calculate(list_1, list_2):
    total = 0
    while list_1:
        value_1 = list_1.pop()
        value_2 = list_2.pop()
        total += abs(value_1 - value_2)
    return total


def calculate2(list_1, list_2):
    total = 0
    for value in list_1:
        total += value * list_2.count(value)
    return total


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    l1, l2 = prepare_lists(data)
    result1 = calculate(l1.copy(), l2.copy())
    print(f"The total distance between lists is {result1}.")

    result2 = calculate2(l1, l2)
    print(f"The similarity score is {result2}.")

    assert result1 == 1651298
    assert result2 == 21306195

