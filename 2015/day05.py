#!/usr/bin/env python3
"""
https://adventofcode.com/2015/day/5
"""
from tools.input import read_input

FILENAME_INPUT = "day05.input.txt"


def has_not_naughty_part(line) -> bool:
    for part in ("ab", "cd", "pq", "xy"):
        if part in line:
            return False
    return True


def has_vowels(line) -> bool:
    vowels_count = 0
    for vowel in "aeiou":
        vowels_count += line.count(vowel)
    return 3 <= vowels_count


def has_double(line) -> bool:
    for i, l in enumerate(line[:-1], start=1):
        if l == line[i]:
            return True
    return False


def any_two_letters(line):
    for i in range(len(line) - 1):
        if 2 <= line.count(line[i : i + 2]):
            return True
    return False


def has_separator(line):
    for i in range(len(line) - 2):
        if line[i] == line[i + 2]:
            return True
    return False


def calculate(data, conditions) -> int:
    count_nice = 0
    for line in data.split("\n"):
        if all((condition(line) for condition in conditions)):
            count_nice += 1
    return count_nice


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    c = has_not_naughty_part, has_vowels, has_double
    result1 = calculate(data, c)
    print(f"{result1} strings are nice.")

    c = any_two_letters, has_separator
    result2 = calculate(data, c)
    print(f"For new rules {result2} strings are nice.")

    assert result1 == 238

# 431 too high
