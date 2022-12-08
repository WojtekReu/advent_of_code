#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/4
"""

with open('day04_input.txt', "r") as f:
    data = f.read()

how_many = 0
overlap = 0
for line in data.split("\n"):
    first = second = None
    for s_numbers in line.split(","):
        begin, end = s_numbers.split("-")
        section = [n for n in range(int(begin), int(end) + 1)]
        if not first:
            first = section
        else:
            second = section

    if first[0] <= second[0] and first[-1] >= second[-1]:
        how_many += 1
    elif second[0] <= first[0] and second[-1] >= first[-1]:
        how_many += 1

    if (
            first[0] <= second[0] <= first[-1]
            or second[0] <= first[0] <= second[-1]
            # first[0] <= second[-1] <= first[-1]
            # or second[0] <= first[-1] <= second[-1]
    ):
        overlap += 1

print(f"how many {how_many} and overlap {overlap}")
