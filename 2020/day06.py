#!/usr/bin/env python3
"""
https://adventofcode.com/2020/day/6
"""
from functools import reduce

from tools.input import read_input

FILENAME_INPUT = "day06.input.txt"


def count_different_questions(text_part: str) -> int:
    return len(set(text_part.replace("\n", "")))


def count_common_questions(text_part: str) -> int:
    return len(reduce(lambda i, j: set(i) & set(j), text_part.split()))


def calculate(data):
    different_question_sum = 0
    common_question_sum = 0
    for text_part in data.split("\n\n"):
        different_question_sum += count_different_questions(text_part)
        common_question_sum += count_common_questions(text_part)

    return different_question_sum, common_question_sum


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    result1, result2 = calculate(data)
    print(f"The sum for all different questions in groups is {result1}.")
    print(f"The sum for all common questions for any person in group is {result2}.")

    assert result1 == 6583
    assert result2 == 3290
