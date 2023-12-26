#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/10
real time  0m0,116s
"""
from itertools import count
from typing import Self

import sys

sys.setrecursionlimit(140 * 140)

FILENAME = "day10.input.txt"


class Pipe:
    char: str
    x: int
    y: int
    is_counted = False
    grid: list
    previous: [Self] = None
    next: [Self] = None

    def __init__(self, c):
        self.char = c
        self.adjacent: list[Self] = []

    def __repr__(self):
        return f"<{self.char}>"

    def is_start_pipe(self):
        return True if self.char == "S" else False

    def calculate_pipe_len(self):
        self.previous = self.adjacent[1]
        self.next = self.adjacent[0]
        len_value = self.next.go_to_next(self)
        return len_value

    def join(self, y_a: int, x_a: int):
        try:
            p_next = self.grid[y_a][x_a]
            self.adjacent.append(p_next)
        except IndexError:
            pass

    def find_adjacent(self, y, x):
        if self.char == "|":
            self.join(y + 1, x)
            self.join(y - 1, x)
        elif self.char == "-":
            self.join(y, x + 1)
            self.join(y, x - 1)
        elif self.char == "L":
            self.join(y - 1, x)
            self.join(y, x + 1)
        elif self.char == "J":
            self.join(y - 1, x)
            self.join(y, x - 1)
        elif self.char == "7":
            self.join(y, x - 1)
            self.join(y + 1, x)
        elif self.char == "F":
            self.join(y, x + 1)
            self.join(y + 1, x)

    def go_to_next(self, p_previous):
        self.previous = p_previous

        for adjacent in self.adjacent:
            if adjacent.is_start_pipe() and not p_previous.is_start_pipe():
                self.next = adjacent
                return 2  # start_pipe and this pipe
            if adjacent is not p_previous:
                self.next = adjacent
                return adjacent.go_to_next(self) + 1

    def change_to_tile(self):
        self.char = "S"
        if self.adjacent[0].char == "F" and self.adjacent[1].char == "7":
            self.char = "-"
        elif self.adjacent[0].char == "|" and self.adjacent[1].char == "|":
            self.char = "|"
        else:
            raise Exception(
                f"Error: can not find char for '{self.adjacent[0].char}', '{self.adjacent[0].char}'."
            )

    def is_going_down(self):
        previous = self.previous
        if self.char == "|" and previous.y < self.y:
            return True
        elif self.char == "L" and self.x == previous.x:
            return True
        elif self.char == "F" and self.y == previous.y:
            return True
        return False

    def is_going_up(self):
        previous = self.previous
        if self.char == "|" and self.y < previous.y:
            return True
        elif self.char == "7" and self.x == previous.x:
            return True
        elif self.char == "J" and self.y == previous.y:
            return True
        return False

    def count_space(self):
        count_space = 0
        counter = count(1)
        if self.is_going_down():
            while True:
                next_p = self.grid[self.y][self.x - next(counter)]
                if next_p.previous or next_p.is_counted:
                    break
                next_p.is_counted = True
                count_space += 1
        elif self.is_going_up():
            while True:
                next_p = self.grid[self.y][self.x + next(counter)]
                if next_p.previous or next_p.is_counted:
                    break
                next_p.is_counted = True
                count_space += 1
        return count_space

    def go_clockwise(self, count_space, reverse_directions=False):
        if reverse_directions:
            new_next = self.previous
            self.previous = self.next
            self.next = new_next
        count_space += self.count_space()
        if self.is_start_pipe() and count_space > 0:
            return count_space
        return self.next.go_clockwise(count_space, reverse_directions)


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    grid = [[Pipe(c) for c in l] for l in data.split("\n")]
    start_pipe = None
    for y, row in enumerate(grid):
        for x, p in enumerate(row):
            if p.is_start_pipe():
                start_pipe = p
                p.x = x
                p.y = y
                p.grid = grid
                continue

            p.x = x
            p.y = y
            p.grid = grid
            p.find_adjacent(y, x)

    # to find adjacent for 'S' you must replace char on '-' and then on '|' to check all neighbours.
    start_pipe.char = "|"
    start_pipe.find_adjacent(start_pipe.y, start_pipe.x)
    start_pipe.char = "-"
    start_pipe.find_adjacent(start_pipe.y, start_pipe.x)
    start_pipe.adjacent = [p2 for p2 in start_pipe.adjacent if start_pipe in p2.adjacent]
    start_pipe.char = "S"

    return start_pipe, grid


def get_highest_left_point(grid):
    for row in grid:
        for p in row:
            if p.previous:
                # Because this is most top and most left corner of path, original char is 'F'
                p.char = "S"
                return p


def calculate(start_point: Pipe, grid: list):
    res = start_point.calculate_pipe_len()

    start_point.change_to_tile()

    start_point = get_highest_left_point(grid)

    count_pipes = 0
    if start_point.next.char in "-7":
        len_value = start_point.go_clockwise(count_pipes)
    else:  # char is one of 'J|L'
        len_value = start_point.go_clockwise(count_pipes, True)

    return res / 2, len_value


if __name__ == "__main__":
    data = read_input(FILENAME)
    sp, g = prepare(data)
    res1, res2 = calculate(sp, g)
    print(f"Number of steps for the farthest point from the starting position is {int(res1)}.")
    print(f"Tiles enclosed by loop is {res2}.")
    assert res1 == 6725
    assert res2 == 383
