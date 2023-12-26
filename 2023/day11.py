#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/11
pypy3 real time  0m0,629s
"""
from collections import namedtuple
from itertools import count, combinations

FILENAME = "day11.input.txt"
EXPANSION_SIZE_P1 = 2
EXPANSION_SIZE_P2 = 1_000_000

Galaxy = namedtuple("Galaxy", ["y", "x", "nr"])


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def get_expansion_coordinates(data_rows: list) -> tuple[list, list]:
    expand_y = [y for y, row in enumerate(data_rows) if "#" not in row]
    expand_x = [x for x, column in enumerate(zip(*data_rows)) if "#" not in column]
    return expand_y, expand_x


def prepare(data: str) -> tuple[list, tuple[list, list]]:
    data_rows = data.split("\n")
    expand_coords = get_expansion_coordinates(data_rows)
    universe = []
    counter = count(1)
    for y, row in enumerate(data_rows):
        for x, c in enumerate(row):
            if c == "#":
                universe.append(Galaxy(y, x, next(counter)))
    return universe, expand_coords


def expand_distance(v1, v2, expand_list, expansion_size):
    dv = 0
    for expand_value in expand_list:
        if v1 < v2:
            if v1 < expand_value < v2:
                dv += expansion_size
        elif v2 < expand_value < v1:
            dv += expansion_size
    return dv


def calculate_distance(g1, g2, expansion_size, expand_y, expand_x):
    dx = abs(g1.x - g2.x) + expand_distance(g1.x, g2.x, expand_x, expansion_size)
    dy = abs(g1.y - g2.y) + expand_distance(g1.y, g2.y, expand_y, expansion_size)
    return dx + dy


def calculate(universe, expand_coords, expansion_size):
    distances = {}
    for g1, g2 in combinations(universe, 2):
        if g1 is not g2:
            distance_key = tuple(sorted((g1.nr, g2.nr)))
            if distance_key not in distances:
                distances[distance_key] = calculate_distance(
                    g1, g2, expansion_size, *expand_coords
                )

    d_sum = sum(distances.values())
    return d_sum


if __name__ == "__main__":
    data = read_input(FILENAME)
    u, ec = prepare(data)
    result = calculate(u, ec, EXPANSION_SIZE_P1 - 1)
    print(f"For expansion size {EXPANSION_SIZE_P1} the sum of galaxies distances is {result}.")
    assert result == 9556896

    result2 = calculate(u, ec, EXPANSION_SIZE_P2 - 1)
    print(f"For expansion size {EXPANSION_SIZE_P2} the sum of galaxies distances is {result2}.")
    assert result2 == 685038186836
