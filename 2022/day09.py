#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/9
"""
import math

with open('day09_input.txt', "r") as f:
    data = f.read()

class Position:
    x = 0
    y = 0

    def __init__(self, is_head):
        if is_head:
            self.tail = Position(False)


positions = [(0, 0)]


class Move:
    x = 0
    y = 0
    x_dir = 0
    y_dir = 0

    def __init__(self, line):
        self.positions = []
        self.unique_positions = []
        words = line.split()
        self.count = int(words[1])
        self.direction = words[0]
        if self.direction == "R":
            self.x_dir = 1
        elif self.direction == "U":
            self.y_dir = 1
        elif self.direction == "L":
            self.x_dir = -1
        elif self.direction == "D":
            self.y_dir = -1

    def go(self, h):
        x_new = h.x + self.x_dir * self.count
        y_new = h.y + self.y_dir * self.count
        for number in range(self.count):
            h.x = h.x + 1 * self.x_dir
            h.y = h.y + 1 * self.y_dir

            t = h.tail
            if 1 < abs(t.x - h.x):
                t.x = t.x + 1 * self.x_dir
                t.y = h.y
            if 1 < abs(t.y - h.y):
                t.y = t.y + 1 * self.y_dir
                t.x = h.x

            p = t.x, t.y
            if p not in positions:
                positions.append(p)


head = Position(True)

for line in data.split("\n"):
    print(line)
    m = Move(line)
    m.go(head)


print(f"Total {len(positions)}.")
