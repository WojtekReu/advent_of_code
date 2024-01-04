#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/23
pypy3 real time  0m7,359s
"""
from collections import namedtuple, defaultdict, deque
from copy import deepcopy
from typing import Any

FILENAME_TEST = "day23.test.txt"
FILENAME_INPUT = "day23.input.txt"


class Point:
    is_finish: bool = False
    visited: set = set()
    step: int = 0
    def __init__(self, y, x, c):
        self.y = y
        self.x = x
        self.c = c
        self.adjacent: list = []
        self.nodes: list[tuple[Point, int]] = []

    def __repr__(self):
        return f"<{self.y},{self.x} {self.c}>"

    def add_adjacent(self, p_next, has_slopes=True):
        if has_slopes:
            if (
                (self.c == ">" and self.x != p_next.x - 1)
                or (self.c == "<" and self.x != p_next.x + 1)
                or (self.c == "v" and self.y != p_next.y - 1)
                or (self.c == "^" and self.y != p_next.y + 1)
            ):
                return
        if p_next.c != "#":
            self.adjacent.append(p_next)

    def is_node(self):
        return bool(2 < len(self.adjacent) or self.is_finish or (self.y == 0 and self.x == 1))


    def go_next(self, step):
        longest_path = 0
        self.visited.add(self)
        if self.is_finish:
            self.visited.remove(self)
            return step

        for point_next, distance in self.nodes:
            if point_next not in self.visited:
                res = point_next.go_next(step + distance)
                if longest_path < res:
                    longest_path = res

        self.visited.remove(self)

        return longest_path

def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str, has_slopes):
    grid = [[Point(y, x, c) for x, c in enumerate(line)] for y, line in enumerate(data.split("\n"))]

    y_max = len(grid) - 1
    for row in grid:
        for point in row:
            if point.c != '#':
                point.add_adjacent(grid[point.y][point.x - 1], has_slopes)
                point.add_adjacent(grid[point.y][point.x + 1], has_slopes)
                point.add_adjacent(grid[point.y - 1][point.x], has_slopes)
                if point.y < y_max:
                    point.add_adjacent(grid[point.y + 1][point.x], has_slopes)

                if point.y == 0:
                    point_start: Point = point
                elif point.y == y_max:
                    point_end: Point = point

    return point_start, point_end, grid


def show(grid, longest_path_runner):
    node_count = 0
    for row in grid:
        for p in row:
            coords = f"{p.y},{p.x}"
            # if coords in longest_path_runner.visited:
            #     print("O", end="")
            if 2 < len(p.adjacent):
                node_count += 1
                print(len(p.adjacent), end="")
            else:
                print(p.c, end="")
        print()

    print("count nodes: ", node_count)


Node = namedtuple('Node', ['p1', 'p2', 'length'])

def calculate(point_start, point_end, grid):
    longest_path = 0
    point_end.is_finish = True
    node = Node(point_start, point_start, 0)
    queue = deque()
    queue.append(node)

    while queue:
        to_remove = []
        is_break = False
        for i, node3 in enumerate(queue):
            for j, node4 in enumerate(queue):
                if node3.p2 is node4.p2 and node3 is not node4:
                    node3.p1.nodes.append((node4.p1, node4.length + node3.length))
                    node4.p1.nodes.append((node3.p1, node4.length + node3.length))
                    to_remove.append(i)
                    to_remove.append(j)
                    is_break = True
                    break
            if is_break:
                break


        for i in sorted(to_remove, reverse=True):
            del queue[i]

        node = queue.popleft()
        if node.p2.is_node():
            if node.p2 is not point_start and node.p1 is not point_end:
                node.p1.nodes.append((node.p2, node.length))
            if node.p1 is not point_start and node.p2 is not point_end:
                node.p2.nodes.append((node.p1, node.length))

            for p_next in node.p2.adjacent:
                if p_next not in p_next.visited:
                    queue.append(Node(node.p2, p_next, 1))

        else:
            for p_next in node.p2.adjacent:
                if p_next not in node.p2.visited or (p_next.is_node() and p_next is not node.p1):
                    queue.append(Node(node.p1, p_next, node.length + 1))

        node.p2.visited.add(node.p2)

    Point.visited = set()

    longest_path = point_start.go_next(0)

    return longest_path, point_start


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    # ps, pe, grid = prepare(data, True)
    # res1, _ = calculate(ps, pe, grid)
    # print(f"For the P1 the longest hike is {res1} steps long.")

    ps, pe, grid = prepare(data, False)
    res2, lpr = calculate(ps, pe, grid)
    # show(grid, lpr)
    print(f"For the P2 the longest hike is {res2} steps long.")

    # assert res1 == 2362
    assert res2 == 6538

