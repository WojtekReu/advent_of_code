#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/23
"""
from typing import Self
from itertools import cycle

PROPOSES = ("N", "S", "W", "E")
ROUNDS = 10
ROUNDS_P2 = 10000


def read_input():
    with open('day23.input.txt', "r") as f:
    # with open('day23.test.txt', "r") as f:
        data = f.read()

    area = []
    for row_nr, line in enumerate(data.split("\n")):
        row = []
        area.append(row)
        for col_nr, sign in enumerate(line):
            row.append(sign)

    elves_count = 0
    next_elf = None
    positions = set()
    area = [r for r in reversed(area)]
    for row_nr, row in enumerate(area):
        for col_nr, sign in enumerate(row):
            if sign == "#":
                elf = Elf(col_nr, row_nr)
                positions.add((col_nr, row_nr))
                elf.nr = elves_count + 1
                elf.next = next_elf
                next_elf = elf
                elves_count += 1

    # area_row_len = len(area[0])
    # area_len = len(area)
    # print(f"{area_len=}   {area_row_len=}   {elves_count=} , {len(positions)}")

    return elf, positions


def get_range(positions):
    x0 = min(positions, key=lambda x: x[0])[0]
    x1 = max(positions, key=lambda x: x[0])[0]
    y0 = min(positions, key=lambda x: x[1])[1]
    y1 = max(positions, key=lambda x: x[1])[1]
    return x0, x1, y0, y1


def show(positions):
    x0, x1, y0, y1 = get_range(positions)
    area_str = '\n'
    for y in range(y0, y1 + 1):
        row_str = ''
        for x in range(x0, x1 + 1):
            if (x, y) in positions:
                row_str += '#'
            else:
                row_str += '.'
        area_str = f"{row_str}\n" + area_str
    return area_str


def simulate(first_elf, positions, rounds):
    dirs = list(PROPOSES)

    for round_nr in range(1, rounds + 1):
        want_to_move = {}
        elf = first_elf
        while elf:
            if elf.have_neighbours(positions):
                elf.scan_area(positions, want_to_move, dirs)
            elf = elf.next

        if not want_to_move:
            break

        elf = first_elf
        while elf:
            elf.go_to_direction(positions, want_to_move)
            elf = elf.next

        dir1 = dirs[0]
        dirs = dirs[1:]
        dirs.append(dir1)
        # print(show(positions))

    x0, x1, y0, y1 = get_range(positions)
    x1 += 1
    y1 += 1
    # print(f"number of rounds i {round_nr=}")
    # print(f"Rectangle: x:({x0},{x1}) y:({y0},{y1})")

    pos_number = (x1 - x0) * (y1 - y0)

    dot_area = pos_number - len(positions)
    return round_nr, dot_area


class Elf:
    nr: int
    next: Self | None = None
    proposed_coords: tuple | None = None
    direction = cycle(PROPOSES)

    def __init__(self, col, row):
        self.x = int(col)
        self.y = int(row)

    def __repr__(self):
        return f"<# {self.x},{self.y}>"

    def have_neighbours(self, positions) -> bool:
        neigh = (
            (self.x - 1, self.y + 1), (self.x, self.y + 1), (self.x + 1, self.y + 1),
            (self.x - 1, self.y), (self.x + 1, self.y),
            (self.x - 1, self.y - 1), (self.x, self.y - 1), (self.x + 1, self.y - 1),
        )
        for pos in neigh:
            if pos in positions:
                return True
        return False

    def scan_area(self, positions, want_to_move, dirs):

        for direction in dirs:
            # direction = self.next_direction()
            for pos in self.pos_directions(direction):
                if pos in positions:
                    break
            else:
                self.proposed_coords = self.coords_for_direction(direction)
                if self.proposed_coords in want_to_move:
                    want_to_move[self.proposed_coords] += 1
                else:
                    want_to_move[self.proposed_coords] = 1
                break

    def next_direction(self):
        return next(self.direction)

    def pos_directions(self, direction):
        return self.neighbours()[direction]

    def neighbours(self):
        neigh = {
            "N": ((self.x - 1, self.y + 1), (self.x, self.y + 1), (self.x + 1, self.y + 1)),
            "S": ((self.x - 1, self.y - 1), (self.x, self.y - 1), (self.x + 1, self.y - 1)),
            "W": ((self.x - 1, self.y - 1), (self.x - 1, self.y), (self.x - 1, self.y + 1)),
            "E": ((self.x + 1, self.y - 1), (self.x + 1, self.y), (self.x + 1, self.y + 1)),
        }
        return neigh

    def coords_for_direction(self, direction):
        match direction:
            case "N":
                return self.x, self.y + 1
            case "S":
                return self.x, self.y - 1
            case "W":
                return self.x - 1, self.y
            case "E":
                return self.x + 1, self.y

    def go_to_direction(self, positions, want_to_move):
        if self.proposed_coords and want_to_move[self.proposed_coords] == 1:
            positions.remove((self.x, self.y))
            positions.add(self.proposed_coords)
            self.x, self.y = self.proposed_coords
        self.proposed_coords = None


first_elf_obj, positions_set = read_input()
# print(show(area_data))
rounds, result = simulate(first_elf_obj, positions_set, ROUNDS)
print(f"After {rounds} rounds empty ground tiles number is {result}.")

first_elf_obj, positions_set = read_input()
rounds2, result2 = simulate(first_elf_obj, positions_set, ROUNDS_P2)
print(f"After {rounds2} rounds no Elf moved. Empty ground tiles number is {result2}.")
