#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/24
pypy3 real time 0m4,438s
"""
from collections import namedtuple
from itertools import combinations
from sympy import Symbol, solve

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
        b1 = h1.y - a1 * h1.x
        b2 = h2.y - a2 * h2.x

        try:
            p_x = (b2 - b1) / (a1 - a2)
        except ZeroDivisionError:
            continue  # hails don't collide, theirs paths are parallel.
        p_y = a1 * p_x + b1

        if check_area[0] <= p_x <= check_area[1] and check_area[0] <= p_y <= check_area[1]:
            if (h1.vx < 0 and p_x < h1.x) or (0 < h1.vx and h1.x < p_x):  # is h1 in the future
                if (h2.vx < 0 and p_x < h2.x) or (0 < h2.vx and h2.x < p_x):  # is h2 in the future
                    collides.append((h1, h2))
                    # print(f"{h1}, {h2} =    {round(p_x, 3)}, {round(p_y, 3)}       {a1 = } {a2 = }   {b1 = }  {b2 = }")

    return len(collides)


def calculate2(hailstones):
    h1 = hailstones[0]
    h2 = hailstones[1]
    h3 = hailstones[2]

    cr_x = Symbol("cr_x")
    cr_y = Symbol("cr_y")
    cr_z = Symbol("cr_z")
    cr_vx = Symbol("cr_vx")
    cr_vy = Symbol("cr_vy")
    cr_vz = Symbol("cr_vz")
    t1 = Symbol("t1")
    t2 = Symbol("t2")
    t3 = Symbol("t3")

    equation = [
        cr_x + cr_vx * t1 - h1.x - h1.vx * t1,
        cr_y + cr_vy * t1 - h1.y - h1.vy * t1,
        cr_z + cr_vz * t1 - h1.z - h1.vz * t1,

        cr_x + cr_vx * t2 - h2.x - h2.vx * t2,
        cr_y + cr_vy * t2 - h2.y - h2.vy * t2,
        cr_z + cr_vz * t2 - h2.z - h2.vz * t2,

        cr_x + cr_vx * t3 - h3.x - h3.vx * t3,
        cr_y + cr_vy * t3 - h3.y - h3.vy * t3,
        cr_z + cr_vz * t3 - h3.z - h3.vz * t3,
    ]
    solution = solve(equation, cr_x, cr_y, cr_z, cr_vx, cr_vy, cr_vz, t1, t2, t3)
    print(solution)
    return sum(solution[0][:3])


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    h = prepare(data)

    res1 = calculate(h, CHECK_AREA)
    print(f"The number of intersections that occur within the test area is {res1}.")
    assert res1 == 20963

    res2 = calculate2(h)
    print(f"When you add up X, Y, and Z coordinates of the initial position you get {res2}.")
    assert res2 == 999782576459892
