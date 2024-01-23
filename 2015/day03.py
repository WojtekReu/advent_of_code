#!/usr/bin/env python3
"""
https://adventofcode.com/2015/day/3
"""
from collections import namedtuple

from tools.input import read_input

FILENAME_INPUT = "day03.input.txt"

Deliverer = namedtuple("Deliverer", ["x", "y"])


def go_next_house(x: int, y: int, instruction) -> Deliverer:
    if instruction == ">":
        x += 1
    elif instruction == "<":
        x -= 1
    elif instruction == "^":
        y += 1
    elif instruction == "v":
        y -= 1
    return Deliverer(x, y)


def calculate(data, is_robo_santa=False) -> int:
    positions = set()
    positions.add("0,0")
    santa = Deliverer(0, 0)
    robo_santa = Deliverer(0, 0) if is_robo_santa else None
    for i, c in enumerate(data):
        if robo_santa and i % 2:
            robo_santa = go_next_house(robo_santa.x, robo_santa.y, c)
            positions.add(f"{robo_santa.x},{robo_santa.y}")
            continue
        santa = go_next_house(santa.x, santa.y, c)
        positions.add(f"{santa.x},{santa.y}")

    return len(positions)


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    result1 = calculate(data)
    print(f"{result1} houses received at least one present.")

    result2 = calculate(data, True)
    print(
        f"When Santa and Robo-Santa deliver presents {result2} houses will receive at least one present."
    )

    assert result1 == 2565
    assert result2 == 2639
