#!/usr/bin/env python3
"""
https://adventofcode.com/2015/day/9
real time  0m0,169s
"""
from itertools import pairwise, permutations

from tools.input import read_input

FILENAME_INPUT = "day09.input.txt"
FILENAME_TEST = "day09.test.txt"


def prepare(data):
    places = set()
    distances = {}
    for line in data.split("\n"):
        p1, _, p2, _, value = line.split()
        distances[p1, p2] = int(value)
        distances[p2, p1] = int(value)
        places.add(p1)
        places.add(p2)

    return places, distances


def calculate(places, distances, func) -> int:
    distance_before = 9999999 if func is min else 0
    l = len(places)
    for places_order in permutations(places, l):
        distance = sum(distances[pair] for pair in pairwise(places_order))
        distance_before = func(distance_before, distance)  # func is min or max

    return distance_before


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    p, d = prepare(data)
    result1 = calculate(p, d, min)
    print(f"The distance of the shortest route is {result1}.")

    result2 = calculate(p, d, max)
    print(f"The distance of the longest route is {result2}.")

    assert result1 == 207
    assert result2 == 804
