#!/usr/bin/env python3
"""
https://adventofcode.com/2020/day/3
"""
from tools.input import grid_one, read_input

FILENAME_INPUT = "day03.input.txt"
SLOPES = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))


def calculate(tree_map: list[str], right: int = 3, down: int = 1) -> int:
    trees = 0
    step = 0
    for i, line in enumerate(tree_map):
        if i % down:
            continue
        try:
            square = line[step]
        except IndexError:
            step = step - len(line)
            square = line[step]
        if square == "#":
            trees += 1
        step += right
    return trees


def calculate2(tree_map: list[str]):
    multiply = 1
    for right, down in SLOPES:
        trees = calculate(tree_map, right, down)
        multiply *= trees
    return multiply


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    tm = grid_one(data)
    result1 = calculate(tm)
    print(f"You would encounter {result1} trees.")

    result2 = calculate2(tm)
    print(
        f"You get {result2} if you multiply together encountered trees on each of the listed slopes."
    )

    assert result1 == 193
    assert result2 == 1355323200
