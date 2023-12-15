#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/15
"""
FILENAME_TEST = "day15.test.txt"
FILENAME_INPUT = "day15.input.txt"


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    seq = data.split(",")
    return seq


def calculate(seq):
    seq_sum = 0
    for k in seq:
        current_value = 0
        for c in k:
            current_value += ord(c)
            current_value *= 17
            current_value %= 256
        seq_sum += current_value
    return seq_sum


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    d = prepare(data)
    res1 = calculate(d)
    print(f"The sum of the result is {res1}.")
    assert res1 == 504036
