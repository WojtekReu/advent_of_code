#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/05
real time   0m0,042s
"""
FILENAME = "day05.input.txt"
import re


class PlantMap:
    def __init__(self, source, destination):
        self.source_category = source
        self.destination_category = destination
        self.ranges = []

    def __repr__(self):
        return f"<{self.source_category}-to-{self.destination_category}>"

    def create_maps(self, destination_range, source_range, range_length):
        self.ranges.append(
            (
                Range(destination_range, o_range=range_length, name=self.destination_category),
                Range(source_range, o_range=range_length, name=self.source_category),
            )
        )

    def convert(self, seed, seeds):
        for destination_range, source_range in self.ranges:
            seed, is_in_range = source_range.has_value(seed, seeds)
            if is_in_range:
                seed = source_range.shift(seed, destination_range)
                return seed
        return seed


class Range:
    def __init__(self, start, end=None, o_range=None, name="-"):
        self.start = start
        self.end = end if end else start + o_range
        self.range = o_range if o_range else end - start
        self.name = name

    def __repr__(self):
        return f"<{self.start} - {self.end}: {self.name}={self.range}>"

    def __gt__(self, other):
        return bool(self.start < other)

    def __lt__(self, other):
        return bool(other < self.end)

    def set_end(self, value):
        self.end = value
        self.calc_range()

    def set_start(self, value):
        self.start = value
        self.calc_range()

    def calc_range(self):
        self.range = self.end - self.start

    def has_value(self, seed, seeds):
        is_in_range = False
        if isinstance(seed, int):
            if self.start <= seed <= self.end:
                is_in_range = True
        else:
            if self.start <= seed.end - 1 and seed.start < self.end - 1:
                is_in_range = True
                if seed.start < self.start:
                    seeds.append(Range(seed.start, end=self.start, name="seeds"))
                    seed.set_start(self.start)
                if self.end < seed.end:
                    seeds.append(Range(self.end, end=seed.end, name="seeds"))
                    seed.set_end(self.end)

        return seed, is_in_range

    def shift(self, other, destination_range):
        shift_value = destination_range.start - self.start
        if isinstance(other, int):
            return other + shift_value
        else:
            new_start = other.start + shift_value
            new_end = other.end + shift_value
            new_range = Range(new_start, end=new_end, name="seeds")
            return new_range


def read_input(filename):
    with open(filename, "r") as f:
        return f.read()


def prepare(data):
    seeds = [int(v) for v in data.split("\n")[0][6:].split()]
    plant_maps = []

    for line in data.split("\n")[1:]:
        if line and line[0].isalpha():
            words = re.split("[- ]", line)
            plant_map = PlantMap(words[0], words[2])
            plant_maps.append(plant_map)
        elif line:
            words = [int(x) for x in line.split()]
            plant_map.create_maps(*words)

    for plant_map in plant_maps:
        plant_map.ranges.sort(
            key=lambda x: x[1].start
        )  # x is a tuple(Range, Range); second Range is destination range; destination range has attribute start

    return plant_maps, seeds


def generate_seed_ranges(old_seeds: list) -> list:
    seeds = []
    start_range = None
    for value in old_seeds:
        if start_range:
            seeds.append(Range(start_range, o_range=value, name="seeds"))
            start_range = None
        else:
            start_range = value

    return seeds


def calculate(plant_maps, seeds):
    for p_map in plant_maps:
        seeds_converted = []
        while seeds:
            seed = seeds.pop(0)
            seeds_converted.append(p_map.convert(seed, seeds))

        if p_map.destination_category == "location":
            seed_min = min(seeds_converted)
            if isinstance(seed_min, int):
                return seed_min
            else:
                return seed_min.start
        else:
            seeds = seeds_converted


if __name__ == "__main__":
    data = read_input(FILENAME)
    pm, s = prepare(data)
    result = calculate(pm, s.copy())
    print(f"The lowest location number for seed numbers is {result}.")
    s = generate_seed_ranges(s)

    result2 = calculate(pm, s)
    print(f"The lowest location number for seed ranges is {result2}.")
