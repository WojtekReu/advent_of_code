#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/2
"""
with open("day02.input.txt", "r") as f:
    data = f.read()

horizontal_sum = 0
vertical_sum = 0

for row in data.split("\n"):
    if row.startswith("forward "):
        horizontal_sum += int(row.split()[1])
    elif row.startswith("down "):
        vertical_sum += int(row.split()[1])
    elif row.startswith("up "):
        vertical_sum -= int(row.split()[1])
print(
    f"Horizontal position is {horizontal_sum}, vertical position is {vertical_sum}, multiple is "
    f"{horizontal_sum * vertical_sum}."
)

horizontal_sum = 0
vertical_sum = 0
aim = 0

for row in data.split("\n"):
    if row.startswith("forward "):
        x = int(row.split()[1])
        horizontal_sum += x
        vertical_sum += aim * x
    elif row.startswith("down "):
        aim += int(row.split()[1])
    elif row.startswith("up "):
        aim -= int(row.split()[1])
print(
    f"2 Horizontal position is {horizontal_sum}, vertical position is {vertical_sum}, multiple is "
    f"{horizontal_sum * vertical_sum}."
)
