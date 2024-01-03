#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/18
real time  0m0,289s
"""
from collections import namedtuple
from typing import Self

from shapely import Polygon

FILENAME_TEST = "day18.test.txt"
FILENAME_INPUT = "day18.input.txt"


Point = namedtuple("Point", ["x", "y"])


class Cube:
    next: [Self] = None
    right_site_value: [int] = None
    is_visited = False
    direction: str

    def __init__(self, y: int, x: int, c: str):
        self.y = y
        self.x = x
        self.c = c

    def __repr__(self):
        return f"<{self.c} y={self.y},x={self.x}>"


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    instructions = []
    for y, line in enumerate(data.split("\n")):
        words = line.split()
        instructions.append((words[0], int(words[1]), words[2].strip("()")))
    return instructions


def calculate(instructions):
    x_min = x_max = y_min = y_max = 0
    start_cube = Cube(0, 0, "")
    start_cube.right_site_value = None
    cube = start_cube
    for direction, steps, color in instructions:
        for i in range(steps):
            right_dir = None
            if direction == "U":
                y = cube.y - 1
                x = cube.x
                right_dir = 1
            elif direction == "D":
                y = cube.y + 1
                x = cube.x
                right_dir = -1
            elif direction == "L":
                y = cube.y
                x = cube.x - 1
            elif direction == "R":
                y = cube.y
                x = cube.x + 1
            next_cube = Cube(y, x, color)
            if not next_cube.right_site_value:
                next_cube.right_site_value = right_dir
            if not cube.right_site_value:
                cube.right_site_value = right_dir
            cube.is_visited = True
            cube.next = next_cube
            cube = next_cube
            x_min = min(x_min, x)
            x_max = max(x_max, x)
            y_min = min(y_min, y)
            y_max = max(y_max, y)

    grid = [[None for _ in range(x_max - x_min + 1)] for _ in range(y_max - y_min + 1)]

    for y, row in enumerate(grid):
        for x, v in enumerate(row):
            if not v:
                grid[y][x] = Cube(y, x, "")

    area_sum = 0

    cube = start_cube
    while cube.next:
        cube.y -= y_min
        cube.x -= x_min
        grid[cube.y][cube.x] = cube
        cube = cube.next

    cube = start_cube
    while cube.next:
        area_sum += 1
        if cube.right_site_value:
            c_right = grid[cube.y][cube.x + cube.right_site_value]
            while not c_right.is_visited:
                area_sum += 1
                c_right.is_visited = True
                new_x = c_right.x + cube.right_site_value
                c_right = grid[cube.y][new_x]
        if cube.x == 0 and cube.y == 1:
            break
        cube = cube.next

    # show(grid)
    return area_sum


def calculate2(instructions):
    point = Point(0, 0)  # x, y
    points = [point]
    circumference = 1  # point(0, 0) is 1
    for _, _, encoded_instruction in instructions:
        steps = int(encoded_instruction[1:6], 16)
        circumference += steps
        dx = 0
        dy = 0
        match encoded_instruction[-1]:
            case "0":
                dx = steps
            case "1":
                dy = -steps
            case "2":
                dx = -steps
            case "3":
                dy = steps
        point = Point(point.x + dx, point.y + dy)
        points.append(point)

    polygon = Polygon(points)

    return polygon.area + (circumference + 1) // 2


def show(grid):
    for row in grid:
        for p in row:
            if p.is_visited:
                print("#", end="")
            else:
                print(".", end="")
        print("")


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    i = prepare(data)
    res1 = calculate(i)
    print(f"It could hold {res1} cubic meters of lava.")
    assert res1 == 39039

    res2 = calculate2(i)
    print(f"The lagoon could hold {res2} cubic meters of lava.")
    assert int(res2) == 44644464596918
