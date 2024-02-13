#!/usr/bin/env python3
"""
https://adventofcode.com/2015/day/8
real time  0m0,029s
"""
from tools.input import read_input

FILENAME_INPUT = "day08.input.txt"
FILENAME_TEST = "day08.test.txt"


def calculate(data) -> int:
    total_signs = len(data.replace("\n", ""))
    data = "".join(line[1:-1] for line in data.split("\n"))
    total_chars = len(data.encode("utf-8").decode("unicode_escape"))
    return total_signs - total_chars


def calculate2(data):
    data = data.replace("\\", "\\\\").replace('"', '\\"')
    data = "\n".join(f'"{line}"' for line in data.split("\n"))
    return calculate(data)


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    result1 = calculate(data)
    print(f"Searched number chars is {result1}.")
    result2 = calculate2(data)
    print(f"Searched second number chars is {result2}.")

    assert result1 == 1342
    assert result2 == 2074
