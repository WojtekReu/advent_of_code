#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/22
pypy3 time real  0m6,951s
"""
import re

from tools.input import read_input


FILENAME_INPUT = "day22.input.txt"
FILENAME_TEST_1 = "day22.test.1.txt"
FILENAME_TEST_2 = "day22.test.2.txt"
INITIAL_RANGE = (-50, 51)  # Range will be (-50, 50)


class Cuboid:
    is_enabled = False

    def __init__(self, *args):
        self.x0, self.x1, self.y0, self.y1, self.z0, self.z1 = args

    def __repr__(self):
        return (
            f"{'on' if self.is_enabled else 'off'} "
            f"x={self.x0}..{self.x1},y={self.y0}..{self.y1},z={self.z0}..{self.z1} \t"
            f"{self.x1 - self.x0}, {self.y1 - self.y0}, {self.z1 - self.z0}, v = {self.volume()}"
        )

    def min_coords(self):
        return self.x0, self.y0, self.z0

    def max_coords(self):
        return self.x1, self.y1, self.z1

    def gen_common_cubics(self, cuboid0):
        """
        Generate all common cubics for self and cuboid0
        """
        x0, y0, z0 = map(max, zip(self.min_coords(), cuboid0.min_coords()))
        x1, y1, z1 = map(min, zip(self.max_coords(), cuboid0.max_coords()))
        for x in range(x0, x1):
            for y in range(y0, y1):
                for z in range(z0, z1):
                    yield f"{x},{y},{z}"

    def has_volume(self):
        return self.x0 < self.x1 and self.y0 < self.y1 and self.z0 < self.z1

    def volume(self) -> int:
        return abs(self.x1 - self.x0) * abs(self.y1 - self.y0) * abs(self.z1 - self.z0)

    def common_part(self, cuboid):
        """
        Generate parted cuboids or the same cuboid when there is no common space with self.
        """
        if (
            are_coords_overlaps(self.x0, self.x1, cuboid.x0, cuboid.x1)
            and are_coords_overlaps(self.y0, self.y1, cuboid.y0, cuboid.y1)
            and are_coords_overlaps(self.z0, self.z1, cuboid.z0, cuboid.z1)
        ):
            x0_max = max(self.x0, cuboid.x0)
            x1_min = min(self.x1, cuboid.x1)
            y0_max = max(self.y0, cuboid.y0)
            y1_min = min(self.y1, cuboid.y1)
            coords_tuple = (
                (cuboid.x0, self.x0, cuboid.y0, cuboid.y1, cuboid.z0, cuboid.z1),
                (self.x1, cuboid.x1, cuboid.y0, cuboid.y1, cuboid.z0, cuboid.z1),
                (x0_max, x1_min, cuboid.y0, self.y0, cuboid.z0, cuboid.z1),
                (x0_max, x1_min, self.y1, cuboid.y1, cuboid.z0, cuboid.z1),
                (x0_max, x1_min, y0_max, y1_min, cuboid.z0, self.z0),
                (x0_max, x1_min, y0_max, y1_min, self.z1, cuboid.z1),
            )
            for coords in coords_tuple:
                parted_cuboid = Cuboid(*coords)
                if parted_cuboid.has_volume():
                    yield parted_cuboid

        else:
            yield cuboid


def are_coords_overlaps(a0, a1, b0, b1) -> bool:
    """
    For any axes cuboids don't overlap when last coord cuboid_B is less than first coord cuboid_A
    or last coord cuboid_A is less than first coord cuboid_B.
    """
    return not (b1 < a0 or a1 < b0)


def prepare(data: str):
    cuboids = []
    for line in data.split("\n"):
        words = line.split()
        nums = []
        for word in re.split("=|\.|,", words[1]):
            try:
                nums.append(int(word))
            except ValueError:
                pass
        cuboid = Cuboid(
            # increase by 1 all second coord value
            nums[0],  # x0
            nums[1] + 1,  # x1
            nums[2],  # y0
            nums[3] + 1,  # y1
            nums[4],  # z0
            nums[5] + 1,  # z1
        )
        cuboid.is_enabled = bool(words[0] == "on")
        cuboids.append(cuboid)

    return cuboids


def calculate(cuboids):
    cuboid0 = Cuboid(
        INITIAL_RANGE[0],
        INITIAL_RANGE[1],
        INITIAL_RANGE[0],
        INITIAL_RANGE[1],
        INITIAL_RANGE[0],
        INITIAL_RANGE[1],
    )
    cuboid_volume = set()

    for cuboid in cuboids:
        # print(cuboid)
        if cuboid.is_enabled:
            for cubic in cuboid.gen_common_cubics(cuboid0):
                cuboid_volume.add(cubic)
        else:
            for cubic in cuboid.gen_common_cubics(cuboid0):
                try:
                    cuboid_volume.remove(cubic)
                except KeyError:
                    pass
    return len(cuboid_volume)


def filter_cuboids_on(cuboids: list) -> list:
    """
    For any cuboid "on" add to cuboids_on but for cuboid "off" check if any cuboid already
    in cuboids_on overlaps it, and if yes, split it and add only not overlap parts.
    """
    cuboids_on = []
    while cuboids:
        cuboid = cuboids.pop(0)
        if cuboid.is_enabled:
            cuboids_on.append(cuboid)
        else:
            new_cuboids_on = []
            for cuboid_on in cuboids_on:
                new_cuboids_on += cuboid.common_part(cuboid_on)
            cuboids_on = new_cuboids_on

    return cuboids_on


def remove_common_space_cuboids(cuboids: list) -> list:
    """
    For all cuboid combinations check if any overlap with other on the list. Cuboid which overlap
    split, drop common parts and rest add to check list.
    """
    cuboids_checked = []
    while cuboids:
        cuboid = cuboids.pop(0)

        cuboids_checked_for_this_one = []
        while cuboids:
            cuboid2 = cuboids.pop(0)
            cuboids_checked_for_this_one += cuboid.common_part(cuboid2)
        cuboids = cuboids_checked_for_this_one
        cuboids_checked.append(cuboid)
    return cuboids_checked


def calculate2(cuboids):
    cuboids = filter_cuboids_on(cuboids)
    cuboids = remove_common_space_cuboids(cuboids)
    total_volume = sum(cuboid.volume() for cuboid in cuboids)
    return total_volume


def main(filename):
    data = read_input(filename)
    c = prepare(data)
    result1 = calculate(c)
    print(f"{result1} cubes are in space range -50, 50.")

    result2 = calculate2(c)
    print(f"{result2} cubes are in whole reactor.")
    assert result1 == 602574
    assert result2 == 1288707160324706


if __name__ == "__main__":
    main(FILENAME_INPUT)
