#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/25
real time  0m4,566s
"""
from typing import Self

from tools.input import read_input, BasePoint

FILENAME_TEST = "day25.test.txt"
FILENAME_INPUT = "day25.input.txt"


class Point(BasePoint):
    right: Self
    down: Self

    def add_next_point(self, grid, y_max, x_max):
        x = self.x + 1 if self.x < x_max else 0
        self.right = grid[self.y][x]

        y = self.y + 1 if self.y < y_max else 0
        self.down = grid[y][self.x]

    def move_right(self, blocked_0_position=False) -> bool:
        if self.right.x == 0 and blocked_0_position:
            return False
        if self.c == ">" and self.right.c == ".":
            self.c = "."
            self.right.c = ">"
            return True
        return False

    def move_down(self, blocked_positions=None) -> [int]:
        if self.down.y == 0 and blocked_positions and self.x in blocked_positions:
            return

        if self.c == "v" and self.down.c == ".":
            self.c = "."
            self.down.c = "v"
            return self.x


def show(grid):
    for row in grid:
        print("".join(p.c for p in row))


def prepare(data: str):
    grid = [[Point(y, x, c) for x, c in enumerate(line)] for y, line in enumerate(data.split("\n"))]

    y_max = len(grid) - 1
    x_max = len(grid[0]) - 1

    for row in grid:
        for p in row:
            p.add_next_point(grid, y_max, x_max)

    return grid


def calculate(grid):
    move_count = 0
    is_moved = True
    while is_moved:
        # print(f"\nAfter {move_count} steps:")
        # show(grid)
        move_count += 1
        is_moved = False
        for row in grid:
            skip_right = False
            is_0_position_locked = False
            for p in row:
                if skip_right:
                    is_moved = True
                    skip_right = False
                else:
                    skip_right = p.move_right(is_0_position_locked)
                    if p.x == 0 and skip_right:
                        is_0_position_locked = True

        skip_down = []
        first_row_blocked_positions = []
        for row in grid:
            for p in row:
                if p.x in skip_down:
                    skip_down.remove(p.x)
                else:
                    p_moved_down = p.move_down(first_row_blocked_positions)
                    if p_moved_down is not None:
                        skip_down.append(p_moved_down)
                        is_moved = True
                        if p.y == 0:
                            first_row_blocked_positions.append(p.x)

    return move_count  # the last iteration is without move


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    g = prepare(data)
    result = calculate(g)
    print(f"The first step when no sea cucumbers move is {result}.")
    assert result == 504
