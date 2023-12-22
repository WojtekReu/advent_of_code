#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/22
"""
from collections import namedtuple, defaultdict

FILENAME_TEST = "day22.test.txt"
FILENAME_INPUT = "day22.input.txt"


El = namedtuple("El", ["x", "y", "z"])


class Brick:
    contains: set
    is_locking = False

    def __init__(self, l):
        begin, end = l.split("~")
        self.x, self.y, self.z = (int(v) for v in begin.split(","))
        self.e_x, self.e_y, self.e_z = (int(v) for v in end.split(","))
        self.calc_contains()

    def __repr__(self):
        return f"<{self.x},{self.y},{self.z} - {self.e_x},{self.e_y},{self.e_z}>"

    @property
    def len_z(self):
        return self.e_z - self.z + 1

    def calc_contains(self):
        self.contains = set()
        for x in range(self.x, self.e_x + 1):
            for y in range(self.y, self.e_y + 1):
                for z in range(self.z, self.e_z + 1):
                    self.contains.add(El(x, y, z))

    def move(self, distance):
        self.z -= distance
        self.e_z -= distance
        self.contains = set(El(el.x, el.y, el.z - distance) for el in self.contains)

    def horizontal(self):
        if self.z == self.e_z:
            for el in self.contains:
                yield el
        else:
            yield max(self.contains, key=lambda e: e.z)


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    bricks = [Brick(line) for line in data.split("\n")]
    return bricks


def bricks_go_down(bricks: list[Brick]):
    bricks.sort(key=lambda b: b.z)
    x_max = max(bricks, key=lambda b: b.x).x
    y_max = max(bricks, key=lambda b: b.y).y
    z_area = {f"{x},{y}": 1 for x in range(x_max + 1) for y in range(y_max + 1)}
    for brick in bricks:
        distances = []
        for el in brick.contains:
            coords = f"{el.x},{el.y}"
            distance = el.z - z_area[coords]
            distances.append(distance)
        d_min = min(distances)
        brick.move(d_min)

        for el in brick.horizontal():
            coords = f"{el.x},{el.y}"
            z_area[coords] = el.z + 1


def bricks_locked(bricks):
    bricks.sort(key=lambda b: b.z)

    z_max = max(bricks, key=lambda b: b.z).z
    z_areas = defaultdict(dict)

    for brick in bricks:
        for el in brick.contains:
            z_areas[el.z][f"{el.x},{el.y}"] = brick

    for brick in sorted(bricks, key=lambda b: b.z, reverse=True):
        possible_locking_block = set()
        for el in brick.contains:
            try:
                brick_under = z_areas[el.z - 1][f"{el.x},{el.y}"]
            except KeyError:
                continue
            if brick_under is brick:
                continue
            possible_locking_block.add(brick_under)

        if len(possible_locking_block) == 1:
            brick_under = list(possible_locking_block)[0]
            brick_under.is_locking = True

    result = len([b for b in bricks if b.is_locking])

    return len(bricks) - result


def show(bricks):
    for b in sorted(bricks, key=lambda b: b.z, reverse=True):
        print(b, b.is_locking)


def calculate(bricks):
    bricks_go_down(bricks)
    res = bricks_locked(bricks)
    # show(bricks)
    return res


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    b = prepare(data)
    res1 = calculate(b)

    print(f"You can remove one from {res1} stack and other bricks don't move.")
