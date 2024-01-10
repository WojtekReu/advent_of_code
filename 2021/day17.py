#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/17
pypy3 real time  0m0,250s
"""
from collections import namedtuple

from tools.input import read_input


FILENAME_INPUT = "day17.input.txt"
FILENAME_TEST = "day17.test.txt"

Target = namedtuple("Target", ["x_min", "x_max", "y_min", "y_max"])


def prepare(data: str) -> Target:
    x0 = x1 = y0 = y1 = None
    for word in data.split():
        if word.startswith("x="):
            x0, x1 = map(int, [nr for nr in word.strip("x=,").split(".") if nr])
        elif word.startswith("y="):
            y0, y1 = map(int, [nr for nr in word.strip("y=,").split(".") if nr])
    if x0 is None or x1 is None or y0 is None or y1 is None:
        raise Exception("Wrong input data")
    return Target(x0, x1, y0, y1)


def simulate(target: Target, dx: int, dy: int) -> [int]:
    x = y = y_max = 0
    while target.y_min < y and x < target.x_max:
        x += dx
        y += dy
        y_max = max(y_max, y)
        if target.x_min <= x <= target.x_max and target.y_min <= y <= target.y_max:
            return y_max
        if 0 < dx:
            dx -= 1
        elif dx < 0:
            dx += 1
        dy -= 1


def calculate(target: Target) -> tuple[int, int, int, int]:
    y_position_max = x_velocity = y_velocity = hit_count = 0
    for x in range(1, target.x_max + 1):
        for y in range(target.y_min, target.x_max + 1):
            y_max = simulate(target, x, y)
            if y_max is not None:
                hit_count += 1
                if y_position_max < y_max:
                    y_position_max = y_max
                    x_velocity = x
                    y_velocity = y

    return y_position_max, x_velocity, y_velocity, hit_count


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    t = prepare(data)
    y_pm, x_v, y_v, hc = calculate(t)
    print(f"The highest y position is {y_pm} for initial velocity of {x_v},{y_v}.")
    print(f"{hc} distinct initial velocity values cause the probe to be within the target area.")

    assert y_pm == 5671
    assert hc == 4556
