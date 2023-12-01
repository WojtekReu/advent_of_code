#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/01
"""
import re

FILENAME = "day01.input.txt"

WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def read_input(filename):
    with open(filename, "r") as f:
        return f.read()


def calculate(data, include_words=False):
    calibration = 0
    for line in data.split("\n"):
        if include_words:
            for word, val in WORDS.items():
                line = line.replace(word, word + str(val) + word)
        nums = list(filter(lambda x: x.isdigit(), line))
        calibration += int(f"{nums[0]}{nums[-1]}")
    return calibration


if __name__ == "__main__":
    data = read_input(FILENAME)
    result = calculate(data)
    print(f"Sum of all of the calibration values is {result}.")
    result = calculate(data, True)
    print(f"In second task sum is {result}.")
