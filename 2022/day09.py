#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/9
"""
RUN_DRAWER_COUNT = 0

with open('day09_input.txt', "r") as f:
    data = f.read()


class Position:
    x = 0
    y = 0
    tail = None

    def __init__(self, knot_count, knot_number, positions):
        self.visited_positions = positions
        self.nr = knot_number - knot_count
        if knot_count:
            self.tail = Position(knot_count - 1, knot_number, positions)

    def run(self, move):
        for number in range(move.count):
            self.x = self.x + 1 * move.x_dir
            self.y = self.y + 1 * move.y_dir

            if self.tail:
                self.tail.shift(self)
            else:
                p = self.x, self.y
                if p not in self.visited_positions:
                    self.visited_positions.append(p)

    def shift(self, previous):
        if 1 < abs(self.x - previous.x):
            direction = 1 if self.x < previous.x else -1
            self.x = self.x + 1 * direction
            if self.y != previous.y:
                direction = 1 if self.y < previous.y else -1
                self.y = self.y + 1 * direction
        if 1 < abs(self.y - previous.y):
            direction = 1 if self.y < previous.y else -1
            self.y = self.y + 1 * direction
            if self.x != previous.x:
                direction = 1 if self.x < previous.x else -1
                self.x = self.x + 1 * direction

        if self.tail:
            self.tail.shift(self)
        else:
            p = self.x, self.y
            if p not in self.visited_positions:
                self.visited_positions.append(p)


class Move:
    x_dir = 0
    y_dir = 0

    def __init__(self, line):
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


class Drawer:
    x_min = -3
    x_max = 10
    y_min = -3
    y_max = 10
    positions = None

    def __init__(self, position: Position, positions):
        self.visited_positions = positions
        self.current_positions = []
        self.add_point(position)
        self.draw()

    def add_point(self, position):
        self.current_positions.append({
            'name': position.nr if position.nr else 'H',
            'x': position.x,
            'y': position.y,
        })
        self.x_min = min(self.x_min, position.x)
        self.x_max = max(self.x_max, position.x)
        self.y_min = min(self.y_min, position.y)
        self.y_max = max(self.y_max, position.y)
        if position.tail:
            self.add_point(position.tail)

    def draw(self):
        for col in reversed(range(self.y_min, self.y_max)):
            for row in range(self.x_min, self.x_max):
                char = 's' if col == row == 0 else '.'
                for position in self.visited_positions:
                    if position[0] == row and position[1] == col:
                        char = '#'
                for position in reversed(self.current_positions):
                    if position['x'] == row and position['y'] == col:
                        char = position['name']
                print(char, end="")
            print()


def go_calculate(tails_number):
    positions = [(0, 0)]
    head = Position(tails_number, tails_number, positions)

    for i, line in enumerate(data.split("\n")):
        m = Move(line)
        head.run(m)
        if i < RUN_DRAWER_COUNT:
            print(line)
            Drawer(head, positions)
    print(f"The tail visited {len(positions)} for rope length {tails_number}.")


go_calculate(tails_number=1)

go_calculate(tails_number=9)
