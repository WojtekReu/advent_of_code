#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/24
pypy3 real time 0m0,232s
"""
from collections import namedtuple
from itertools import combinations

FILENAME_TEST = "day24.test.txt"
FILENAME_INPUT = "day24.input.txt"

CHECK_AREA_TEST = (7, 27)
CHECK_AREA = (200_000_000_000_000, 400_000_000_000_000)

HailStone = namedtuple("HailStone", ["x", "y", "z", "vx", "vy", "vz"])


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    hailstones = []
    for line in data.split("\n"):
        hailstone = HailStone(*(int(v) for v in line.replace("@", ",").split(",")))
        hailstones.append(hailstone)
    return hailstones


def calculate(hailstones, check_area):
    collides = []
    for h1, h2 in combinations(hailstones, 2):
        a1 = h1.vy / h1.vx
        a2 = h2.vy / h2.vx
        b1 = -a1 * h1.x + h1.y
        b2 = -a2 * h2.x + h2.y

        try:
            p_x = (b2 - b1) / (a1 - a2)
        except ZeroDivisionError:
            continue
        p_y = a1 * p_x + b1

        if check_area[0] <= p_x <= check_area[1] and check_area[0] <= p_y <= check_area[1]:
            if (h1.vx < 0 and p_x < h1.x) or (0 < h1.vx and h1.x < p_x):  # is h1 in the future
                if (h2.vx < 0 and p_x < h2.x) or (0 < h2.vx and h2.x < p_x):  # is h2 in the future
                    collides.append((h1, h2))
                    # print(f"{h1}, {h2} =    {round(p_x, 3)}, {round(p_y, 3)}       {a1 = } {a2 = }   {b1 = }  {b2 = }")

    return len(collides)


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    h = prepare(data)
    res1 = calculate(h, CHECK_AREA)
    print(f"The number of intersections that occur within the test area is {res1}.")

    assert res1 == 20963
