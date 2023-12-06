#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/03
"""
from collections import defaultdict

FILENAME = "day03.input.txt"


def read_input(filename):
    with open(filename, "r") as f:
        return [[c for c in line] for line in f.read().split("\n")]


def check1(val):
    return bool(not val.isdigit() and val != ".")


def check2(val):
    return bool(not val.isdigit() and val == "*")


def is_adjacent(y, x, max_y, max_x, matrix, check):
    if 0 < x:
        if check(matrix[y][x - 1]):
            return y, x - 1
    if x < max_x:
        if check(matrix[y][x + 1]):
            return y, x + 1
    if 0 < y:
        if check(matrix[y - 1][x]):
            return y - 1, x
    if y < max_y:
        if check(matrix[y + 1][x]):
            return y + 1, x
    if 0 < x and 0 < y:
        if check(matrix[y - 1][x - 1]):
            return y - 1, x - 1
    if 0 < x and y < max_y:
        if check(matrix[y + 1][x - 1]):
            return y + 1, x - 1
    if x < max_x and 0 < y:
        if check(matrix[y - 1][x + 1]):
            return y - 1, x + 1
    if x < max_x and y < max_y:
        if check(matrix[y + 1][x + 1]):
            return y + 1, x + 1


def calculate(matrix):
    nr = ""
    sum_values = 0
    max_y = len(matrix) - 1
    adjacent = False
    for y, line in enumerate(matrix):
        max_x = len(line) - 1
        for x, c in enumerate(line):
            if c.isdigit():
                nr = f"{nr}{c}"
                if not adjacent:
                    adjacent = is_adjacent(y, x, max_y, max_x, matrix, check1)
            elif nr:
                value = int(nr)
                nr = ""
                if adjacent:
                    sum_values += value
                    adjacent = False
    return sum_values


def calculate2(matrix):
    nr = ""
    elements = defaultdict(list)
    max_y = len(matrix) - 1
    adjacent = False
    for y, line in enumerate(matrix):
        max_x = len(line) - 1
        for x, c in enumerate(line):
            if c.isdigit():
                nr = f"{nr}{c}"
                if not adjacent:
                    adjacent = is_adjacent(y, x, max_y, max_x, matrix, check2)
            else:
                if nr:
                    value = int(nr)
                    nr = ""
                    elements[adjacent].append(value)
                    adjacent = False

    sum_values = 0
    for v_list in elements.values():
        if len(v_list) == 2:
            sum_values += v_list[0] * v_list[1]
    return sum_values


if __name__ == "__main__":
    data = read_input(FILENAME)
    result = calculate(data)
    print(f"The sum of all of the part numbers in teh engine schematic is {result}.")
    result2 = calculate2(data)
    print(f"The sum of all the gear rations in your engine schematic is {result2}.")
