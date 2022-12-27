#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/17
"""
from copy import deepcopy
from itertools import cycle

TUNNEL_WIDTH = 7
POSITION_X0 = 2 + 1  # air + border
HEIGHT_A = 3
ROCKS_P1 = 2022
ROCKS_P2 = 1_000_000_000_000
Y_ABOVE_BOTTOM = 4


def read_input() -> tuple:
    with open('day17.input1.txt', "r") as f:
        data = f.read()

    figures = [Figure(nr, str_data) for nr, str_data in enumerate(data.split("\n\n"))]

    with open('day17.input2.txt', "r") as f:
    # with open('day17.test.txt', "r") as f:
        data = f.read()

    return figures, data.rstrip()


def create_tunnel():
    tunnel = []
    tunel_str = '|·······|\n' \
                '|·······|\n' \
                '|·······|\n' \
                '|·······|\n' \
                '|·······|\n' \
                '|·······|\n' \
                '|·······|\n' \
                '+-------+\n'
    for line in reversed(tunel_str.split()):
        tunnel.append([char for char in line])
    return tunnel


def tunnel_extend(tunnel):
    for y, row in enumerate(tunnel):
        if '#' not in row and '-' not in row:
            break

    y += HEIGHT_A
    while len(tunnel) < y + Y_ABOVE_BOTTOM:
        tunnel.append(['|', '·', '·', '·', '·', '·', '·', '·', '|'])

    return y


def show(tunnel):
    tetris = ''
    for line in reversed(tunnel):
        tetris += ''.join(line) + "\n"
    return tetris


def simulate(figures, jets, rock_counts):
    figures_cycle = cycle(figures)
    jets_cycle = cycle(jets)
    tunnel = create_tunnel()
    x = POSITION_X0
    y = Y_ABOVE_BOTTOM
    figure = next(figures_cycle)
    rock = figure.create(tunnel, x, y)
    while rock_counts:
        rock.move(tunnel, next(jets_cycle))
        if rock.can_down(tunnel):
            rock.down(tunnel)
        else:
            rock_counts -= 1
            figure = next(figures_cycle)
            y = tunnel_extend(tunnel)
            rock = figure.create(tunnel, x, y)

    # print(show(tunnel))
    return y - Y_ABOVE_BOTTOM


class Position:

    def __init__(self, data: list[list[int]]):
        self.data = deepcopy(data)

    def __add__(self, other):
        for y, row in enumerate(self.data):
            for x, el in enumerate(row):
                self.data[y][x] = el + other

    def __mul__(self, other):
        for y, row in enumerate(self.data):
            for x, el in enumerate(row):
                self.data[y][x] = el * other


class Figure:
    nr: int
    height: int
    visual: list
    turn_count = 0

    def __init__(self, nr: int, str_representation: str):
        self.nr = nr
        self.visual = []
        self.numeric = []
        self.right_edge = []
        self.left_edge = []
        for row, line in enumerate(reversed(str_representation.split())):
            self.visual.append(line.strip())

            self.left_edge.append(line.index('#'))
            self.right_edge.append(max([i for i, c in enumerate(line) if c == "#"]))

        self.height = len(self.visual)
        self.width = len(self.visual[0])
        self.bottom_edge = [0] * self.width

        for row, line in enumerate(str_representation.split()):
            for col, char in enumerate(line):
                if char == "#":
                    self.bottom_edge[col] = self.height - row - 1

    def __repr__(self):
        return f"<{self.nr}>"

    def __str__(self):
        return "\n".join(self.visual)

    def create(self, tunnel: list, x: int, y):
        rock = Rock(self, x, y)
        t_height = len(tunnel)
        for r_y, row in enumerate(rock.figure.visual):
            for r_x, char in enumerate(row):
                if char == '#':
                    tunnel[r_y+y][r_x+x] = '#'
        return rock


class Rock:
    position: Position

    def __init__(self, figure, x, y):
        self.x = x
        self.y = y
        self.figure: Figure = figure

    def __repr__(self):
        return f"({self.x},{self.y})[{self.figure.width},{self.figure.height}]>"

    def move(self, tunnel: list, dir_str):
        direction = 1
        edge = self.figure.right_edge
        if dir_str == '<':
            direction = -1
            edge = self.figure.left_edge

        for dy, edge_nr in enumerate(edge):
            x = self.x + edge_nr + direction
            y = self.y + dy
            if tunnel[y][x] != '·':
                return

        for r_y, row in enumerate(self.figure.visual):
            for r_x, cel in enumerate(row):
                if cel == '#':
                    tunnel[r_y+self.y][r_x+self.x] = '·'

        self.x += direction

        for r_y, row in enumerate(self.figure.visual):
            for r_x, cel in enumerate(row):
                if cel == '#':
                    tunnel[r_y+self.y][r_x+self.x] = '#'

    def can_down(self, tunnel: list):
        for dx, edge_nr in enumerate(self.figure.bottom_edge):
            x = self.x + dx
            y = self.y + edge_nr - 1
            if tunnel[y][x] != '·':
                return False
        return True

    def down(self, tunnel: list):
        for r_y, row in enumerate(self.figure.visual):
            for r_x, cel in enumerate(row):
                if cel == '#':
                    tunnel[r_y+self.y][r_x+self.x] = '·'

        self.y -= 1

        for r_y, row in enumerate(self.figure.visual):
            for r_x, cel in enumerate(row):
                if cel == '#':
                    tunnel[r_y+self.y][r_x+self.x] = '#'


rocks_data, jets_data = read_input()
tower_height = simulate(rocks_data, jets_data, ROCKS_P1)

print(f"Tower has {tower_height} units height.")


def show_rocks(rocks):
    for r in rocks:
        print(str(r))
        print()

