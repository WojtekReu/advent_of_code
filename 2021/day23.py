#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/23
for TEST.1 pypy3 real time  0m32,314s
for INPUT.1 pypy3 real time  5m4,298s
for TEST.2 pypy3 real time  7m55,127s
for INPUT.2 pypy3 real time  47m33,320s
"""
from itertools import cycle
from typing import Generator

from tools.input import read_input


FILENAME_INPUT_1 = "day23.input.1.txt"
FILENAME_INPUT_2 = "day23.input.2.txt"
FILENAME_TEST_1 = "day23.test.1.txt"
FILENAME_TEST_2 = "day23.test.2.txt"
ENERGY_MATRIX = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}
DESTINATION_COLUMNS = {
    "A": 3,
    "B": 5,
    "C": 7,
    "D": 9,
}


class Position:
    right = None
    left = None
    down = None
    up = None

    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x
        self.amphipod = None

    def __repr__(self):
        return f"({self.y},{self.x})"

    def find_adjacent(self, burrow):
        for position in burrow:
            if position.y == self.y and position.x == self.x + 1:
                self.right = position
            elif position.y == self.y and position.x == self.x - 1:
                self.left = position
            elif position.y == self.y + 1 and position.x == self.x:
                self.down = position
            elif position.y == self.y - 1 and position.x == self.x:
                self.up = position


class Hallway(Position):
    def __init__(self, y: int, x: int):
        super().__init__(y, x)

    def __repr__(self):
        return f"H{super().__repr__()}"


class SideRoom(Position):
    def __init__(self, y: int, x: int, destination: str):
        super().__init__(y, x)
        self.destination = destination

    def __repr__(self):
        return f"S{self.destination}{super().__repr__()}"


class Amphipod:
    amphipods = []
    min_energy = {"value": 99999}
    used_energy = 0

    def __init__(self, char, position):
        self.type = char
        self.energy_per_step = ENERGY_MATRIX[char]
        self.position: Position = position
        self.start_position = position
        self.middle_position = None
        self.middle_position_energy = None

    def __repr__(self):
        return f"Amph:{self.type} -> {self.position})"

    def next_position(
        self, position: Position, direction: str, energy: int
    ) -> tuple[Position, int]:
        return getattr(position, direction), energy + self.energy_per_step

    def go_up(self) -> tuple[Position, int]:
        energy = 0
        position = self.start_position
        while position.up and position.up.amphipod is None:
            position, energy = self.next_position(position, "up", energy)
        return position, energy

    def set_position(self, position: Position, energy: int):
        self.position.amphipod = None
        if isinstance(self.position, Hallway):
            self.middle_position = self.position
            self.middle_position_energy = self.used_energy
        self.position = position
        self.used_energy = energy
        position.amphipod = self

    def back_to_previous(self):
        if isinstance(self.position, Hallway):
            self.position.amphipod = None
            self.position = self.start_position
            self.used_energy = 0
            self.position.amphipod = self
        elif self.position is not self.start_position:
            self.position.amphipod = None
            self.position = self.middle_position
            self.used_energy = self.middle_position_energy
            self.position.amphipod = self

    def is_looking_side_room(self) -> bool:
        if isinstance(self.position, Hallway) or self.position.destination != self.type:
            return True

        position_down = self.position.down
        while position_down:
            if position_down.amphipod and position_down.amphipod.type != position_down.destination:
                return True
            position_down = position_down.down

        return False

    def direction_to_site_room(self) -> str:
        if DESTINATION_COLUMNS[self.type] < self.position.x:
            return "left"
        return "right"

    def go_to_site_room(self) -> tuple[Position, int]:
        direction = self.direction_to_site_room()
        position = self.position
        energy = self.used_energy
        while getattr(position, direction) and getattr(position, direction).amphipod is None:
            position, energy = self.next_position(position, direction, energy)
            if position.down and position.down.destination == self.type:
                check_position = position.down
                while check_position:
                    if (
                        check_position.amphipod
                        and check_position.amphipod.type != check_position.destination
                    ):
                        # At least one amphipod is in the wrong Side Room, the correct amphipod
                        # cannot enter until the wrong amphipod leaves that Side Room.
                        return self.position, self.used_energy
                    check_position = check_position.down
                if position.down.amphipod is None:
                    # shouldn't but there is some case when correct amphipod is locking the first
                    # position however next positions are available.
                    while position.down and position.down.amphipod is None:
                        position, energy = self.next_position(position, "down", energy)

                    return position, energy
                break

        return self.position, self.used_energy

    def gen_possible_positions(self) -> Generator:
        if isinstance(self.position, SideRoom):
            position, energy = self.go_up()

            while position.left and position.left.amphipod is None:
                position, energy = self.next_position(position, "left", energy)
                if position.x != 3 and position.x != 5 and position.x != 7 and position.x != 9:
                    yield position, energy

            position, energy = self.go_up()
            while position and position.right and position.right.amphipod is None:
                position, energy = self.next_position(position, "right", energy)
                if position.x != 3 and position.x != 5 and position.x != 7 and position.x != 9:
                    yield position, energy

        else:
            position, energy = self.go_to_site_room()
            yield position, energy

        self.back_to_previous()


def prepare(data: str):
    amphipods_destination = cycle("ABCD")
    burrow = []
    amphipods = []
    for y, line in enumerate(data.split("\n")):
        for x, c in enumerate(line):
            if c == ".":
                burrow.append(Hallway(y, x))
            elif c in "ABCD":
                side_room = SideRoom(y, x, next(amphipods_destination))
                burrow.append(side_room)
                amphipod = Amphipod(c, side_room)
                side_room.amphipod = amphipod
                amphipods.append(amphipod)

    # print(burrow)
    for position in burrow:
        position.find_adjacent(burrow)

    return amphipods


def gen_amphipods(amphipods, previous_amphipod):
    for amphipod in amphipods:
        if amphipod is not previous_amphipod:
            if amphipod.is_looking_side_room():
                yield amphipod


def move_amphipods(amphipods, previous_amphipod) -> [int]:
    for amphipod in gen_amphipods(amphipods, previous_amphipod):
        for position, energy in amphipod.gen_possible_positions():
            if position is amphipod.position:
                break

            amphipod.set_position(position, energy)
            # print(f"{amphipod} ::: {amphipods}")
            if sum(a.used_energy for a in amphipods) < Amphipod.min_energy["value"]:
                move_amphipods(amphipods, amphipod)

    if not [a for a in amphipods if a.is_looking_side_room()]:
        Amphipod.min_energy["value"] = min(
            Amphipod.min_energy["value"], sum([a.used_energy for a in amphipods])
        )

    return Amphipod.min_energy["value"]


def calculate(amphipods: list[Amphipod]):
    try:
        move_amphipods(amphipods, None)
    except KeyboardInterrupt:
        pass
    return Amphipod.min_energy["value"]


def main():
    data = read_input(FILENAME_INPUT_1)
    a = prepare(data)
    result1 = calculate(a)
    print(f"At least {result1} energy is required to organize the amphipods.")
    assert result1 == 19160
    a = prepare(read_input(FILENAME_TEST_2))
    a.reverse()
    result2 = calculate(a)
    print(f"At least {result2} energy is required to organize the amphipods from unfolded diagram.")
    assert result2 == 47232


if __name__ == "__main__":
    main()
