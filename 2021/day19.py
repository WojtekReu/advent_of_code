#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/19
real time  0m4,047s
"""
from collections import deque
from itertools import combinations, permutations, product
from math import prod
from typing import Self

from tools.input import read_input


FILENAME_INPUT = "day19.input.txt"
FILENAME_TEST = "day19.test.txt"
# Each scanner has at least 12 common beacons, this give 11 distances between these beacons.
DISTANCES_MIN = 11


class Beacon:
    def __init__(self, *args):
        self.x, self.y, self.z = args
        self.distances: dict[tuple, Self] = {}

    def __repr__(self):
        return f"B({self.x},{self.y},{self.z})"

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def replaced(self, idx: tuple) -> tuple:
        b = tuple(self)
        return b[idx[0]], b[idx[1]], b[idx[2]]


class Scanner:
    x: [int] = None
    y: [int] = None
    z: [int] = None
    idx: [tuple] = None
    sign: [tuple] = None

    def __init__(self, nr):
        self.beacons = set()
        self.nr = nr

    def __repr__(self):
        return f"S{self.nr}({self.x},{self.y},{self.z})"

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def beacon_from_line(self, line):
        self.beacons.add(Beacon(*map(int, line.split(","))))

    def calculate_distances(self):
        for b1, b2 in combinations(self.beacons, 2):
            distance = get_distance(b1, b2)
            yield distance, b1, b2

    def prepare_distances(self, idx=(0, 1, 2)):
        for distance, b1, b2 in self.calculate_distances():
            distance_with_idx = distance[idx[0]], distance[idx[1]], distance[idx[2]]
            b1.distances[distance_with_idx] = b2
            b2.distances[distance_with_idx] = b1

    def match_the_same_distances(self, scanner0: Self) -> dict[Beacon, Beacon]:
        same_beacons = {}
        for a in scanner0.beacons:
            for b in self.beacons:
                distances_count = sum(1 for d2 in b.distances if d2 in a.distances)
                if DISTANCES_MIN <= distances_count:
                    same_beacons[a] = b
        return same_beacons

    def indexes(self, distance: tuple[int, int, int]) -> tuple[int, int, int]:
        """
        return coords map ex.: (1,2,0) - this swaps coords. For (0,1,2) coords doesn't change.
        """
        for distance_permutation in permutations(distance, 3):
            for beacon1 in self.beacons:
                if distance_permutation in beacon1.distances:
                    yield tuple(map(distance.index, distance_permutation))

    def match_distances(self, scanner0: Self) -> bool:
        for distance, b1, b2 in self.calculate_distances():
            for idx in scanner0.indexes(distance):
                self.prepare_distances(idx)
                same_beacons = self.match_the_same_distances(scanner0)

                for sign in product((1, -1), repeat=3):  # (1,1,1), (-1,1,1), ... ,(-1,-1,-1)  8 elements
                    scanner_coords_before = None
                    if same_beacons:
                        for a3, b3 in same_beacons.items():
                            b3_mapped = [c for c in map(prod, zip(b3.replaced(idx), sign))]
                            scanner_coords = [c for c in map(sum, zip(b3_mapped, a3))]
                            if scanner_coords_before and scanner_coords != scanner_coords_before:
                                # if scanner coords changed sign is wrong. Get next sign.
                                break
                            scanner_coords_before = scanner_coords
                        else:
                            # all beacons in same_beacons gave the same scanner_coords.
                            self.x, self.y, self.z = scanner_coords
                            # for scanner sign is reversed (1,-1,1) -> (-1,1,-1)
                            self.sign = tuple(-1 * c for c in sign)
                            similar_distances_b3 = set(same_beacons.values())
                            for b3 in self.beacons:
                                if b3 not in similar_distances_b3:
                                    b3_mapped = [
                                        c for c in map(prod, zip(b3.replaced(idx), self.sign))
                                    ]
                                    a3_bis = [c for c in map(sum, zip(self, b3_mapped))]
                                    scanner0.beacons.add(Beacon(*a3_bis))
                            return True
        return False


def get_distance(b1, b2) -> tuple[int, int, int]:
    return abs(b1.x - b2.x), abs(b1.y - b2.y), abs(b1.z - b2.z)


def prepare(data: str) -> list[Scanner]:
    scanners = []
    for line in data.split("\n"):
        if line.startswith("--- scanner "):
            scanner = Scanner(line.split()[2])
            scanners.append(scanner)
        elif line:
            scanner.beacon_from_line(line)
    return scanners


def calculate(scanners: list) -> int:
    scanners_deque = deque(scanners)
    scanner0 = scanners_deque.popleft()
    scanner0.x = scanner0.y = scanner0.z = 0
    scanner0.prepare_distances()
    while scanners_deque:
        scanner = scanners_deque.popleft()
        if scanner.match_distances(scanner0):
            scanner0.prepare_distances()
        else:
            scanners_deque.append(scanner)
    return len(scanner0.beacons)


def calculate2(scanners: list) -> int:
    max_manhattan_distance = 0
    for s1, s2 in combinations(scanners, 2):
        manhattan_distance = sum(get_distance(s1, s2))
        max_manhattan_distance = max(max_manhattan_distance, manhattan_distance)
    return max_manhattan_distance


def main(filename):
    data = read_input(filename)
    s = prepare(data)
    result1 = calculate(s)
    print(f"There are {result1} beacons.")

    result2 = calculate2(s)
    print(f"The largest Manhattan distance between any two scanners is {result2}.")

    assert result1 == 390
    assert result2 == 13327


if __name__ == "__main__":
    main(FILENAME_INPUT)
