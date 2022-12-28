#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/17
"""
from itertools import cycle

TUNNEL_WIDTH = 7
POSITION_X0 = 2 + 1  # air + border
ROCKS_P1 = 2022 + 1
ROCKS_P2 = 1_000_000_000_000
SHIFT_UP = 7


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
                '+#######+\n'
    for line in reversed(tunel_str.split()):
        tunnel.append([char for char in line])
    return tunnel


def show(tunnel):
    tetris = ''
    for line in reversed(tunnel):
        tetris += ''.join(line) + "\n"
    return tetris


def simulate(figures, jets, rock_counts):
    figures_cycle = cycle(figures)
    jets_cycle = cycle(jets)
    tunnel = create_tunnel()
    cut_off_nr = -1  # Floor also is '#' char
    for _ in range(rock_counts):
        figure: Figure = next(figures_cycle)
        rock, tunnel, y, cut_off_nr = figure.create(tunnel, cut_off_nr, jets_cycle)
        while rock.can_down(tunnel):
            rock.down(tunnel)
            rock.move(tunnel, next(jets_cycle))

        # print(show(tunnel))
        # a = 3444444
    # print(f"{cut_off_nr=}")
    return cut_off_nr + y


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
        self.upper_edge = []
        for row, line in enumerate(reversed(str_representation.split())):
            self.visual.append(line.strip())

            self.left_edge.append(line.index('#'))
            self.right_edge.append(max([i for i, c in enumerate(line) if c == "#"]))

        self.height = len(self.visual)
        self.width = len(self.visual[0])
        self.bottom_edge = [0] * self.width
        self.upper_edge = [0] * self.width

        for row, line in enumerate(str_representation.split()):
            for col, char in enumerate(line):
                if char == "#":
                    self.bottom_edge[col] = self.height - row - 1
                    if not self.upper_edge[col]:
                        self.upper_edge[col] = self.height - row - 1

    def __repr__(self):
        return f"<{self.nr}>"

    def __str__(self):
        return "\n".join(self.visual)

    def create(self, tunnel: list, cut_off_nr, jets_cycle):
        tunnel_len = len(tunnel)
        if 300 < tunnel_len:
            cut_off_nr = cut_off_nr + (tunnel_len - 290)
            tunnel = tunnel[-290:]
        for y, row in enumerate(tunnel):
            if '#' not in row:
                break

        for _ in range(y + SHIFT_UP - tunnel_len):
            tunnel.append(['|', '·', '·', '·', '·', '·', '·', '·', '|'])

        rock = Rock(self, POSITION_X0, y, jets_cycle)
        x = rock.x
        for dy, row in enumerate(rock.figure.visual):
            for dx, char in enumerate(row):
                if char == '#':
                    tunnel[dy + y][dx + x] = '#'
        return rock, tunnel, y, cut_off_nr


class Rock:

    def __init__(self, figure, x, y, jets_cycle):
        for i in range(4):
            dx = 1 if next(jets_cycle) == '>' else -1
            if dx == 1 and x + dx + figure.width < 9:
                x += dx
            elif dx == -1 and 0 < x + dx:
                x += dx
        self.x = x
        self.y = y
        self.figure: Figure = figure

    def __repr__(self):
        return f"({self.x},{self.y})[{self.figure.width},{self.figure.height}]>"

    def move(self, tunnel: list, dir_str):
        direction = 1
        edge = self.figure.right_edge
        other_edge = self.figure.left_edge
        if dir_str == '<':
            direction = -1
            edge = self.figure.left_edge
            other_edge = self.figure.right_edge

        for dy, edge_nr in enumerate(edge):
            if tunnel[self.y + dy][self.x + edge_nr + direction] != '·':
                return

        for dy, edge_nr in enumerate(edge):
            tunnel[self.y + dy][self.x + edge_nr + direction] = '#'
            tunnel[self.y + dy][self.x + other_edge[dy]] = '·'

        self.x += direction

    def can_down(self, tunnel: list):
        for dx, edge_nr in enumerate(self.figure.bottom_edge):
            if tunnel[self.y + edge_nr - 1][self.x + dx] != '·':
                return False
        return True

    def down(self, tunnel: list):
        edge = self.figure.bottom_edge
        other_edge = self.figure.upper_edge
        for dx, edge_nr in enumerate(edge):
            tunnel[self.y + edge_nr - 1][self.x + dx] = '#'
            tunnel[self.y + other_edge[dx]][self.x + dx] = '·'

        self.y -= 1


rocks_data, jets_data = read_input()
tower_height = simulate(rocks_data, jets_data, ROCKS_P1)

print(f"Tower has {tower_height} units height.")
