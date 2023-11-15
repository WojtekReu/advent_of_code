#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/9
"""
import math


def read_input(filename):
    with open(filename, "r") as f:
        raw_data = f.read()

    hmap = []
    for line in raw_data.split():
        hmap.append([int(v) for v in line])

    return hmap


def calculate_risks_sum(hmap):
    risks_sum = 0
    y_max = len(hmap) - 1
    for y, row in enumerate(hmap):
        x_max = len(row) - 1
        for x, val in enumerate(row):
            if 0 < x and row[x - 1] <= val:
                continue
            elif x < x_max and row[x + 1] <= val:
                continue
            elif 0 < y and hmap[y - 1][x] <= val:
                continue
            elif y < y_max and hmap[y + 1][x] <= val:
                continue
            risks_sum += (val + 1)

    return risks_sum


def calculate_basin(y, x, y_max, x_max, hmap):
    neigh = [(y, x)]
    basin = 0
    while neigh:
        y, x = neigh.pop()
        val = hmap[y][x]
        if val < 9:
            basin += 1
            hmap[y][x] = 9
            if 0 < x:
                neigh.append((y, x - 1))
            if x < x_max:
                neigh.append((y, x + 1))
            if 0 < y:
                neigh.append((y - 1, x))
            if y < y_max:
                neigh.append((y + 1, x))

    return basin

def find_3_largest_basins(hmap):
    basins = []
    y_max = len(hmap) - 1
    for y, row in enumerate(hmap):
        x_max = len(row) - 1
        for x, val in enumerate(row):
            basin_size = calculate_basin(y, x, y_max, x_max, hmap)
            basins.append(basin_size)

    return sorted(basins, reverse=True)[:3]


if __name__ == "__main__":
    heightmap = read_input("day09.input.txt")
    result = calculate_risks_sum(heightmap)
    print(f"Sum of risks is {result}.")
    largest_basins = find_3_largest_basins(heightmap)

    print(f"3 largest basins {largest_basins} have multiply value: {math.prod(largest_basins)}")
