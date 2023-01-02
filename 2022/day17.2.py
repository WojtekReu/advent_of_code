#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/17
Run by:
$ pypy3 day17.2.py
"""
from itertools import cycle


TUNNEL_WIDTH = 7
POSITION_X0 = 2
SHIFT_Y0 = 4
SEARCH_Y_START = 6
ROCKS_P1 = 2022
ROCKS_P2 = 1_000_000_000_000
ROCKS_P2_TEST = 1_000_000
SHIFT_UP = 8  # space above last rock + max rock height
CUT_OFF = 27  # cut tetris lines bellow max possible down


def read_input() -> tuple:
    with open('day17.input1.txt', "r") as f:
        data = f.read()

    figures = [Figure(nr, str_data) for nr, str_data in enumerate(data.split("\n\n"))]

    with open('day17.input2.txt', "r") as f:
    # with open('day17.test.txt', "r") as f:
        data = f.read()

    return figures, data.rstrip()


def create_tunnel():
    point_before = None
    for i in range(TUNNEL_WIDTH - 1, -1, -1):
        point = Point(i, 0)
        if point_before:
            point_before.left = point
            point.right = point_before
        point_before = point
    return point


def show(point_corner, rock):
    tetris = ''
    point_down = point_corner
    while point_down:
        point_right = point_down
        while point_right:
            if rock.has(point_right):
                tetris += "@"
            else:
                tetris += point_right.char
            point_right = point_right.right
        point_down = point_down.down
        tetris += "\n"
    return tetris


def simulate(figures, jets, rock_counts):
    figures_cycle = cycle(figures)
    jets_cycle = cycle(jets)
    point_corner = create_tunnel()

    y = -1
    for _ in range(rock_counts):
        figure: Figure = next(figures_cycle)
        rock, point_corner = figure.create(point_corner, y)
        # print(show(point_corner, rock))
        while True:
            char = next(jets_cycle)
            if char == '>':
                rock.go('right')
            else:
                rock.go('left')
            if not rock.go('down'):
                point = rock.stop()
                y = max(point.y, y)
                if CUT_OFF < y - point.y:
                    # free memory from not used objects
                    point_a = point
                    while point:
                        point.down = None
                        point = point.right
                    while point_a:
                        point_a.down = None
                        point_a = point_a.left

                break

    return y + 1


class Figure:
    nr: int
    shift: int = 0
    height: int
    len_points_1: int

    def __init__(self, nr: int, str_representation: str):
        self.nr = nr
        self.visual = []
        self.points = []
        self.arrows = []

        for y, line in enumerate(reversed(str_representation.split())):
            for x, char in enumerate(line):
                if x == 0 and y == 0 and char == '.':
                    self.shift = 1
                if char == '#':
                    self.points.append((y, x))

            self.visual.append(line.strip())

        self.height = len(self.visual)
        self.width = len(self.visual[0])
        point_before = (self.height - 1, 0)

        for point in reversed(self.points):
            arrow = (point[0] - point_before[0], point[1] - point_before[1])
            point_before = point
            self.arrows.append(arrow)

        self.len_points_1 = len(self.points) - 1
        self.visual = tuple(self.visual)
        self.points = tuple(self.points)
        self.arrows = tuple(self.arrows)

    def __repr__(self):
        return f"<{self.nr}>"

    def __str__(self):
        return "\n".join(self.visual)

    def create(self, point_corner, y):
        while point_corner.y < y + SHIFT_UP:
            point = point_corner
            point_before = None
            y_new = point.y + 1

            for i in range(TUNNEL_WIDTH):
                point_above = Point(point.x, y_new)
                point_above.down = point
                if point_before:
                    point_before.right = point_above
                    point_above.left = point_before
                else:
                    point_corner = point_above
                point_before = point_above
                point = point.right

        point_x2 = point_corner.right.right
        start_y = y + SHIFT_Y0
        figure_y = start_y + self.height - 1
        for i in range(SEARCH_Y_START):
            if point_x2.y == figure_y:
                point_figure = point_x2
                break
            point_x2 = point_x2.down

        point = point_figure
        rock_before = None
        for i, arrow in enumerate(self.arrows):
            if arrow[0] == -1:
                point = point.down
            if arrow[1] == -1:
                point = point.left
            elif arrow[1] == 1:
                point = point.right
            elif arrow[1] == 2:
                point = point.right.right
            elif arrow[1] == 3:
                point = point.right.right.right
            rock = Rock()
            rock.point = point
            if rock_before:
                rock.next = rock_before

            rock_before = rock

        rock_first = rock

        return rock_first, point_corner

    def rock_point(self, i, x, y, rock, point_figure):
        point_row = point_figure
        point = point_row
        for dy in range(self.height):
            for dx in range(self.width):
                if x == point.x and y == point.y:
                    rock.point = point
                    if i < self.len_points_1:
                        rock.next = Rock()
                        rock = rock.next
                    return rock
                point = point.right
            point_row = point_row.down
            point = point_row
        raise ValueError(f"Rock not found: i = {i}, ({x},{y})")


class Point:
    char = '.'
    x: int
    y: int
    left = None
    right = None
    down = None

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.char}{self.x},{self.y}"


class Rock:
    point: Point = None
    next = None

    def __repr__(self):
        if self.point:
            return f"R{self.point}"
        return f"R -"

    def go(self, direction: str):
        if direction == 'down':
            point_next = self.point.down
        elif direction == 'left':
            point_next = self.point.left
        elif direction == 'right':
            point_next = self.point.right
        if point_next and point_next.char == '.':
            if self.next:
                if self.next.go(direction):
                    self.point = point_next
                    return True
            else:
                self.point = point_next
                return True

        return False

    def stop(self) -> Point:
        self.point.char = "#"
        if self.next:
            return max(self.next.stop(), self.point, key=lambda p: p.y)
        return self.point

    def has(self, point):
        if self.point is point:
            return True
        elif self.next:
            return self.next.has(point)
        return False


rocks_data, jets_data = read_input()
tower_height = simulate(rocks_data, jets_data, ROCKS_P2_TEST)

print(f"Tower has {tower_height} units height.")
