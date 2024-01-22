#!/usr/bin/env python3
"""
https://adventofcode.com/2015/day/1
"""
from tools.input import read_input

FILENAME_INPUT = "day01.input.txt"


def calculate(data):
    return data.count("(") - data.count(")")


def calculate2(data):
    floor = 0
    for i, c in enumerate(data, start=1):
        floor += 1 if c == "(" else -1
        if floor < 0:
            return i


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    result1 = calculate(data)
    print(f"The instructions takes Santa to the {result1} floor.")

    result2 = calculate2(data)
    print(f"The basement position is {result2}.")

    assert result1 == 138
    assert result2 == 1771
