#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/5
"""
data = []
with open("day05.input.txt", "r") as f:
    for line in f.read().splitlines():
        begin_pair, _, end_pair = line.split()
        x1, y1 = begin_pair.split(",")
        x2, y2 = end_pair.split(",")
        data.append((
            (int(x1), int(y1)), (int(x2), int(y2))
        ))

def calculate_overlapping(data, is_diagonal):
    c_max = 1000
    points = {(x, y): 0 for x in range(c_max) for y in range(c_max)}
    for vent in data:
        if vent[0][0] == vent[1][0] or vent[0][1] == vent[1][1]:
            x_direction = -1 if vent[1][0] < vent[0][0] else 1
            y_direction = -1 if vent[1][1] < vent[0][1] else 1
            for x in range(vent[0][0], vent[1][0] + x_direction, x_direction):
                for y in range(vent[0][1], vent[1][1] + y_direction, y_direction):
                    points[(x, y)] += 1

    count_overlapping = 0
    for k, v in points.items():
        if 1 < v:
            count_overlapping += 1

    return count_overlapping

result = calculate_overlapping(data, is_diagonal=False)

print(f"Overlapping {result} points.")
