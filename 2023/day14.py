#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/14
real time  0m12,822s
"""
from hashlib import md5
from itertools import cycle

import numpy

REQUIRED_CYCLES = 1_000_000_000

FILENAME_TEST = "day14.test.txt"
FILENAME_INPUT = "day14.input.txt"


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    dish = [[c for c in line] for line in data.split()]
    np_dish = numpy.array(dish)
    # From now North is on the left in this program
    np_dish_rotated = numpy.rot90(np_dish)
    return np_dish_rotated


def move_to_bound(row, x):
    if x == 0:
        return
    for i in range(x - 1, -1, -1):
        if row[i] == "O" or row[i] == "#":
            if i + 1 != x:
                row[i + 1] = "O"
                row[x] = "."
            return
        elif i == 0:
            row[i] = "O"
            row[x] = "."
            return


def til_dish(dish):
    for y, row in enumerate(dish):
        for x, el in enumerate(row):
            if el == "O":
                move_to_bound(row, x)


def calculate(dish):
    til_dish(dish)
    return calc_load(dish, "N")


def calc_load(dish, d):
    dish = numpy.rot90(dish, k=direction(d, "c"))
    dish_row_len = len(dish[0])
    total_load = 0
    for row in dish:
        for i, el in enumerate(row):
            if el == "O":
                total_load += dish_row_len - i

    return total_load


def direction(d, s):
    """
    Rotate for calculation or showing
    """
    if s == "s":
        match d:
            case "N":
                return 3
            case "W":
                return 0
            case "S":
                return 1
            case "E":
                return 2
    elif s == "c":  # always rotate to North for calculation
        match d:
            case "N":
                return 0
            case "W":
                return 1
            case "S":
                return 2
            case "E":
                return 3


def show_dish(dish, d):
    print(f"----- {d} --------")
    dish = numpy.rot90(dish, direction(d, "s"))
    dish_str = str(dish).replace("'", "").replace(" ", "")
    print(dish_str)


def gen_hash(dish, d):
    dish_string = d
    for row in dish:
        for c in row:
            dish_string = f"{dish_string}{c}"
    res = md5(dish_string.encode("utf-8")).hexdigest()
    return res


def calculate2(dish):
    dish_hashes = {}
    c = 0
    # Remember North is on the left! See prepare(data) function
    direction_cycle = cycle(("N", "W", "S", "E"))
    for d in direction_cycle:
        til_dish(dish)
        dish_hash = gen_hash(dish, d)
        if dish_hash in dish_hashes:
            break
        else:
            dish_hashes[dish_hash] = c
            c += 1
        dish = numpy.rot90(dish, k=3)

    beginning = dish_hashes[dish_hash]
    repeat = c - beginning
    rest = (REQUIRED_CYCLES * 4 - beginning) % repeat
    print(f"After {c} rotations you have {d} direction.")
    print(
        f"Every {repeat} rotation repetition you have the same O stones position. Its needs {rest} rotation to achieve {REQUIRED_CYCLES}."
    )

    for i in range(rest):
        d = next(direction_cycle)
        til_dish(dish)
        dish = numpy.rot90(dish, k=3)

    # Finish rotation cycle to N direction
    while d != "N":
        d = next(direction_cycle)
        til_dish(dish)
        dish = numpy.rot90(dish, k=3)

    res = calc_load(dish, d)

    # show_dish(dish, d)
    return res


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    mt = prepare(data)
    res1 = calculate(mt)
    print(f"The total load is {res1}.")
    assert res1 == 108918

    res2 = calculate2(mt)
    print(f"After {REQUIRED_CYCLES} cycles the total load is {res2}.")
    assert res2 == 100310
