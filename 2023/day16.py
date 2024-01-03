#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/16
"""
from typing import Self

FILENAME_TEST = "day16.test.txt"
FILENAME_INPUT = "day16.input.txt"


class Point:
    is_visited = False
    visited_directions: list[Self]

    def __init__(self, y, x, c):
        self.y = y
        self.x = x
        self.c = c
        self.paths = {}
        self.visited_directions = []

    def __repr__(self):
        return f"<{self.c},y={self.y} x={self.x}>"

    def add(self, p_input, p_output):
        if p_input and p_output:
            self.paths[p_input] = (p_output,)
            self.paths[p_output] = (p_input,)

    def add_the_split(self, *args):
        if not args[0]:
            return
        self.paths[args[0]] = tuple(x for x in args[1:] if x)

    def join(self, grid, edges):
        if self.c == ".":
            side_1 = get_point(self.y, self.x - 1, grid, edges)
            side_2 = get_point(self.y, self.x + 1, grid, edges)
            self.add(side_1, side_2)
            side_1 = get_point(self.y - 1, self.x, grid, edges)
            side_2 = get_point(self.y + 1, self.x, grid, edges)
            self.add(side_1, side_2)
        elif self.c == "\\":
            side_1 = get_point(self.y, self.x - 1, grid, edges)
            side_2 = get_point(self.y + 1, self.x, grid, edges)
            self.add(side_1, side_2)
            side_1 = get_point(self.y - 1, self.x, grid, edges)
            side_2 = get_point(self.y, self.x + 1, grid, edges)
            self.add(side_1, side_2)
        elif self.c == "/":
            side_1 = get_point(self.y, self.x - 1, grid, edges)
            side_2 = get_point(self.y - 1, self.x, grid, edges)
            self.add(side_1, side_2)
            side_1 = get_point(self.y + 1, self.x, grid, edges)
            side_2 = get_point(self.y, self.x + 1, grid, edges)
            self.add(side_1, side_2)
        elif self.c == "|":
            side_1 = get_point(self.y - 1, self.x, grid, edges)
            side_2 = get_point(self.y + 1, self.x, grid, edges)
            self.add(side_1, side_2)
            side_1 = get_point(self.y, self.x - 1, grid, edges)
            side_2 = get_point(self.y - 1, self.x, grid, edges)
            side_3 = get_point(self.y + 1, self.x, grid, edges)
            self.add_the_split(side_1, side_2, side_3)
            side_1 = get_point(self.y, self.x + 1, grid, edges)
            side_2 = get_point(self.y - 1, self.x, grid, edges)
            side_3 = get_point(self.y + 1, self.x, grid, edges)
            self.add_the_split(side_1, side_2, side_3)
        elif self.c == "-":
            side_1 = get_point(self.y, self.x - 1, grid, edges)
            side_2 = get_point(self.y, self.x + 1, grid, edges)
            self.add(side_1, side_2)
            side_1 = get_point(self.y - 1, self.x, grid, edges)
            side_2 = get_point(self.y, self.x - 1, grid, edges)
            side_3 = get_point(self.y, self.x + 1, grid, edges)
            self.add_the_split(side_1, side_2, side_3)
            side_1 = get_point(self.y + 1, self.x, grid, edges)
            side_2 = get_point(self.y, self.x - 1, grid, edges)
            side_3 = get_point(self.y, self.x + 1, grid, edges)
            self.add_the_split(side_1, side_2, side_3)


class Beem:
    point1: Point
    point2: Point

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def __repr__(self):
        return f"B:{self.point1}->{self.point2};"

    def go(self):
        if self.point2 and self.point1 in self.point2.paths:
            for point in self.point2.paths[self.point1]:
                point.is_visited = True
                if self.point1 not in self.point2.visited_directions:
                    yield Beem(self.point2, point)
            self.point1.is_visited = True
            self.point2.is_visited = True
            self.point2.visited_directions.append(self.point1)


def get_point(y, x, grid, edges) -> [Point]:
    for p in edges:
        if p.x == x and p.y == y:
            return p
    if y < 0 or x < 0 or len(grid) - 1 < y or len(grid[0]) - 1 < x:
        return None
    return grid[y][x]


def show(grid):
    for row in grid:
        for p in row:
            if p.is_visited:
                print("#", end="")
            else:
                print(".", end="")
        print("")


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    grid = [[Point(y, x, c) for x, c in enumerate(line)] for y, line in enumerate(data.split("\n"))]

    edges = []
    y_max = len(grid) - 1
    x_max = len(grid[0]) - 1
    for y in range(y_max):
        p = Point(y, -1, ".")
        edges.append(p)
        p = Point(y, x_max + 1, ".")
        edges.append(p)

    for x in range(x_max):
        p = Point(-1, x, ".")
        edges.append(p)
        p = Point(y_max + 1, x, ".")
        edges.append(p)

    for row in grid:
        for p in row:
            p.join(grid, edges)

    return grid, edges


def calculate(grid, edges):
    results = []
    y_max = len(grid)
    x_max = len(grid[0])
    for ps in edges:
        if ps.x == -1:
            p0 = grid[ps.y][0]
        elif ps.x == x_max:
            p0 = grid[ps.y][x_max - 1]
        elif ps.y == -1:
            p0 = grid[0][ps.x]
        elif ps.y == y_max:
            p0 = grid[y_max - 1][ps.x]

        beem = Beem(ps, p0)
        beems = [beem]
        while beems:
            beem = beems.pop()
            for b in beem.go():
                beems.append(b)

        res = 0
        for row in grid:
            for p in row:
                if p.is_visited:
                    p.is_visited = False
                    res += 1
                p.visited_directions = []

        # print(p0.y, p0.x, res)
        results.append(res)

    return results[0], max(results)


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    g, e = prepare(data)
    res1, res2 = calculate(g, e)
    print(f"{res1} tiles end up being energized.")
    print(f"When start is from any edge point {res2} tiles end up being energized.")
    assert res1 == 7798
    assert res2 == 8026
