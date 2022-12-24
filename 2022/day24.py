#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/24
"""
from typing import Self


def read_input():
    with open('day24.input.txt', "r") as f:
    # with open('day24.test.txt', "r") as f:
        data = f.read()

    valley = []
    before = None
    for row_nr, line in enumerate(reversed(data.split("\n"))):
        row = []
        valley.append(row)
        for col_nr, sign in enumerate(line):
            pos = Position(col_nr, row_nr, sign)
            row.append(pos)
            if sign != '#':
                pos.next = before
                before = pos
                if sign in '^>v<':
                    pos.blizzards.append(sign)

    return valley


def prepare(valley):
    len_valley = len(valley)
    len_valley_row = len(valley[0])
    pos = valley[len_valley - 1][1]
    jump_up_y = len_valley - 2
    jump_right_x = len_valley_row - 2
    jump_down_y = 1
    jump_left_x = 1
    while pos.next:

        if pos.y == jump_down_y and pos.x != jump_right_x:
            # the second condition is for position before finish (x=max-1, y=1)
            y = jump_up_y
        else:
            y = pos.y - 1
            pos.neighbors.append(valley[y][pos.x])
        pos.down = valley[y][pos.x]

        if pos.y == len_valley - 1:
            # The start position has only move down and below start position have to go up also.
            before_start = valley[len_valley - 2][1]
            before_start.up = pos
            before_start.neighbors.append(pos)
            pos = pos.next
            continue

        if pos.y == jump_up_y:
            y = jump_down_y
        else:
            y = pos.y + 1
            pos.neighbors.append(valley[y][pos.x])
        pos.up = valley[y][pos.x]

        if pos.x == jump_right_x:
            x = jump_left_x
        else:
            x = pos.x + 1
            pos.neighbors.append(valley[pos.y][x])
        pos.right = valley[pos.y][x]

        if pos.x == jump_left_x:
            x = jump_right_x
        else:
            x = pos.x - 1
            pos.neighbors.append(valley[pos.y][x])
        pos.left = valley[pos.y][x]

        pos = pos.next

    first_pos = valley[len_valley - 1][1]
    finish_pos = valley[0][len_valley_row - 2]
    finish_pos.up = valley[1][len_valley_row - 2]
    finish_pos.neighbors.append(finish_pos.up)

    return first_pos, finish_pos


def simulate(first_pos, finish_pos, the_first):
    step = 0
    positions_e = {first_pos}
    while True:
        step += 1

        pos = the_first
        while pos:
            pos.move_blizzards()
            pos = pos.next

        pos = the_first
        while pos:
            pos.copy_lists()
            pos = pos.next

        new_positions_e = set()
        for e in positions_e:
            if not e.blizzards:
                # this is 'wait in place' case
                new_positions_e.add(e)

            for neighbour in e.neighbors:
                if not neighbour.blizzards:
                    new_positions_e.add(neighbour)

        if not new_positions_e:
            raise ValueError(f"Error: Empty my positions for step {step}")

        if finish_pos in new_positions_e:
            return step
        else:
            positions_e = new_positions_e


class Position:
    x: int
    y: int
    initial_sign: str
    up: Self
    right: Self
    down: Self
    left: Self
    next: Self | None = None

    def __init__(self, x, y, sign):
        self.x = x
        self.y = y
        self.initial_sign = sign
        self.blizzards = []
        self.new_blizzards = []
        self.neighbors = []  # this has list (up, right, down, left) for position_e.

    def __repr__(self):
        return f"<{self.x},{self.y}>"

    def move_blizzards(self):
        while self.blizzards:
            blizzard = self.blizzards.pop()
            match blizzard:
                case '^':
                    self.up.new_blizzards.append(blizzard)
                case '>':
                    self.right.new_blizzards.append(blizzard)
                case 'v':
                    self.down.new_blizzards.append(blizzard)
                case '<':
                    self.left.new_blizzards.append(blizzard)

    def copy_lists(self):
        self.blizzards = self.new_blizzards
        self.new_blizzards = []


valley_data = read_input()
first_pos_data, finish_pos_data = prepare(valley_data)

steps1 = simulate(first_pos_data, finish_pos_data, first_pos_data)
steps2 = simulate(finish_pos_data, first_pos_data, first_pos_data)
steps3 = simulate(first_pos_data, finish_pos_data, first_pos_data)

steps_sum = steps1 + steps2 + steps3

print(
    f"The first trip takes {steps1} minutes, the trip back takes {steps2} minutes, and the trip"
    f"back to the goal again takes {steps3}, for a total time of {steps_sum} minutes."
)
