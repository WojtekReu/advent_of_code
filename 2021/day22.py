#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/22
pypy3 time real  0m0,788s
"""
import re

from tools.input import read_input


FILENAME_INPUT = "day22.input.txt"
FILENAME_TEST = "day22.test.txt"
INITIAL_RANGE = (-50, 51)  # Range will be (-50, 50)


class Cube:
    is_enabled = False

    def __init__(self, *args):
        self.x0, self.x1, self.y0, self.y1, self.z0, self.z1 = args

    def __repr__(self):
        return f"C({self.x0}..{self.x1},{self.y0}..{self.y1},{self.z0}..{self.z1})"

    def min_coords(self):
        return self.x0, self.y0, self.z0

    def max_coords(self):
        return self.x1, self.y1, self.z1

    def get_positions(self, cube0):
        x0, y0, z0 = map(max, zip(self.min_coords(), cube0.min_coords()))
        x1, y1, z1 = map(min, zip(self.max_coords(), cube0.max_coords()))
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    yield f"{x},{y},{z}"


def prepare(data: str):
    cubes = []
    for line in data.split("\n"):
        words = line.split()
        nums = []
        for c in re.split("=|\.|,", words[1]):
            try:
                nums.append(int(c))
            except ValueError:
                pass
        cube = Cube(*nums)
        cube.is_enabled = bool(words[0] == "on")
        cubes.append(cube)

    return cubes


def calculate(cubes):
    cube0 = Cube(
        INITIAL_RANGE[0],
        INITIAL_RANGE[1],
        INITIAL_RANGE[0],
        INITIAL_RANGE[1],
        INITIAL_RANGE[0],
        INITIAL_RANGE[1],
    )
    cube_r = set()

    for cube in cubes:
        # print(cube)
        if cube.is_enabled:
            for position in cube.get_positions(cube0):
                cube_r.add(position)
        else:
            for position in cube.get_positions(cube0):
                try:
                    cube_r.remove(position)
                except KeyError:
                    pass
    return len(cube_r)


def main(filename):
    data = read_input(filename)
    c = prepare(data)
    result1 = calculate(c)
    print(f"{result1} cubes are on.")


if __name__ == "__main__":
    main(FILENAME_INPUT)
