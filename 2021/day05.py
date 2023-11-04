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
        data.append(((int(x1), int(y1)), (int(x2), int(y2))))


def lines_condition(points: dict, vent: tuple, is_diagonal: bool) -> None:
    if vent[0][1] == vent[1][1]:
        x_direction = -1 if vent[1][0] < vent[0][0] else 1
        for x in range(vent[0][0], vent[1][0] + x_direction, x_direction):
            points[(x, vent[0][1])] += 1
        return

    elif vent[0][0] == vent[1][0]:
        y_direction = -1 if vent[1][1] < vent[0][1] else 1
        for y in range(vent[0][1], vent[1][1] + y_direction, y_direction):
            points[(vent[0][0], y)] += 1
        return

    if is_diagonal:
        if abs(vent[1][0] - vent[0][0]) == abs(vent[1][1] - vent[0][1]):
            x_direction = -1 if vent[1][0] < vent[0][0] else 1
            y_direction = -1 if vent[1][1] < vent[0][1] else 1
            for i, x in enumerate(range(vent[0][0], vent[1][0] + x_direction, x_direction)):
                y = y_direction * i + vent[0][1]
                points[(x, y)] += 1


def calculate_overlapping(data, is_diagonal):
    c_max = 1000
    points = {(x, y): 0 for x in range(c_max) for y in range(c_max)}
    for vent in data:
        lines_condition(points, vent, is_diagonal)

    count_overlapping = 0
    for k, v in points.items():
        if 1 < v:
            count_overlapping += 1

    return count_overlapping


result = calculate_overlapping(data, is_diagonal=False)

print(f"For horizontal and vertical lines overlapping points is {result}.")

result2 = calculate_overlapping(data, is_diagonal=True)

print(f"For horizontal and vertical and diagonal lines overlapping points is {result2}.")
