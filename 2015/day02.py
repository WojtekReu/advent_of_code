#!/usr/bin/env python3
"""
https://adventofcode.com/2015/day/2
"""
from tools.input import read_input

FILENAME_INPUT = "day02.input.txt"


def calculate(data):
    total_paper = total_ribbon = 0
    for line in data.split("\n"):
        l, w, h = tuple(map(int, line.split("x")))
        total_paper += 2 * l * w + 2 * w * h + 2 * h * l + min(l * w, w * h, h * l)
        total_ribbon += sum(dim * 2 for dim in sorted((l, w, h))[:2]) + l * w * h
    return total_paper, total_ribbon


def calculate2(data):
    floor = 0
    for i, c in enumerate(data, start=1):
        floor += 1 if c == "(" else -1
        if floor < 0:
            return i


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    result1, result2 = calculate(data)
    print(f"They should order {result1} total square feet of wrapping paper.")
    print(f"They should order {result2} total feet of ribbon.")

    assert result1 == 1606483
    assert result2 == 3842356
