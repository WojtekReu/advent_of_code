#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/19
real time  0m4,809s
"""
from collections import deque
from itertools import combinations, permutations, product
from math import prod
from typing import Self

from tools.input import read_input


FILENAME_INPUT = "day19.input.txt"
FILENAME_TEST = "day19.test.txt"


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

    def indexes(self, distance: tuple[int, int, int], scanner0: Self):
        for distance_permutation in permutations(distance, 3):
            for beacon in scanner0.beacons:
                if distance_permutation in beacon.distances:
                    idx = tuple(map(distance.index, distance_permutation))
                    beacon2 = beacon.distances[distance_permutation]
                    yield idx, beacon, beacon2

    def match_distances(self, scanner0: Self) -> bool:
        similar_distances = {}
        for distance, b1, b2 in self.calculate_distances():
            for idx, a1, a2 in self.indexes(distance, scanner0):
                self.prepare_distances(idx)
                for a in scanner0.beacons:
                    for b in self.beacons:
                        distances_count = sum(1 for d2 in b.distances if d2 in a.distances)
                        similar_distances[a, b] = distances_count

                matched_beacons = {}
                for k, v in sorted(similar_distances.items(), key=lambda x: x[1], reverse=True):
                    if 11 <= v:
                        matched_beacons[k[0]] = k[1]

                for sign in product((1, -1), repeat=3):
                    before = None
                    if matched_beacons:
                        for a3, b3 in matched_beacons.items():
                            b3_diagonal = [c for c in map(prod, zip(b3.replaced(idx), sign))]
                            d3 = [c for c in map(sum, zip(b3_diagonal, a3))]
                            if before and d3 != before:
                                break
                            before = d3
                        else:
                            self.x, self.y, self.z = d3
                            self.sign = tuple(-1 * c for c in sign)
                            for b3 in self.beacons:
                                if b3 not in matched_beacons.values():
                                    b3_diagonal = [
                                        c for c in map(prod, zip(b3.replaced(idx), self.sign))
                                    ]
                                    a3_bis = [c for c in map(sum, zip(self, b3_diagonal))]
                                    scanner0.beacons.add(Beacon(*a3_bis))
                            return True
        return False

def get_distance(b1, b2):
    return abs(b1.x - b2.x), abs(b1.y - b2.y), abs(b1.z - b2.z)


def prepare(data: str):
    scanners = []
    for line in data.split("\n"):
        if line.startswith("--- scanner "):
            scanner = Scanner(line.split()[2])
            scanners.append(scanner)
        elif line:
            scanner.beacon_from_line(line)
    return scanners


def calculate(scanners: list):
    scanners_deque = deque(scanners)
    scanner0 = scanners_deque.popleft()
    scanner0.x = scanner0.y = scanner0.z = 0
    scanner0.prepare_distances()
    while scanners_deque:
        scanner = scanners_deque.popleft()
        is_found = scanner.match_distances(scanner0)
        if is_found:
            scanner0.prepare_distances()
        else:
            scanners_deque.append(scanner)
    return len(scanner0.beacons)


def calculate2(scanners):
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
