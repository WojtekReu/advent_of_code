#!/usr/bin/env python3
"""
https://adventofcode.com/2015/day/4
real time  0m1,704s
"""
from hashlib import md5
from itertools import count

from tools.input import read_input

FILENAME_INPUT = "day04.input.txt"


def calculate(data, zeros) -> int:
    counter = count()
    input_data = data.encode("utf-8")
    while True:
        number = next(counter)
        result = md5(input_data + str(number).encode("utf-8"))
        if result.hexdigest().startswith(zeros):
            return number


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    result1 = calculate(data, "00000")
    print(f"For string `{data}` the lowest number which gives 5 zeros for md5 is {result1}.")
    result2 = calculate(data, "000000")
    print(f"For string `{data}` the lowest number which gives 6 zeros for md5 is {result2}.")

    assert result1 == 254575
    assert result2 == 1038736
