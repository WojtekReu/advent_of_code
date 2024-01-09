#!/usr/bin/env python3
"""
https://adventofcode.com/2020/day/01
"""
from itertools import combinations
from math import prod

FILENAME_INPUT = "day01.input.txt"
EXPECTED_VALUE = 2020
P1_COMPONENTS_NUMBER = 2
P2_COMPONENTS_NUMBER = 3


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data):
    return [int(nr) for nr in data.split()]


def calculate(numbers: list[int], components_number: int) -> [int]:
    for components in combinations(numbers, components_number):
        if sum(components) == EXPECTED_VALUE:
            return prod(components)


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    ns = prepare(data)
    result1 = calculate(ns, P1_COMPONENTS_NUMBER)
    print(
        f"If you multiply {P1_COMPONENTS_NUMBER} entries which sum is {EXPECTED_VALUE} you get {result1}."
    )

    result2 = calculate(ns, P2_COMPONENTS_NUMBER)
    print(
        f"If you multiply {P2_COMPONENTS_NUMBER} entries which sum is {EXPECTED_VALUE} you get {result2}."
    )
    assert result1 == 567171
    assert result2 == 212428694
