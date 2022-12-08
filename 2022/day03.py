#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/3
"""
from string import ascii_lowercase, ascii_uppercase

with open('day03_input.txt', "r") as f:
    data = f.read()

priority = {}
for i, l in enumerate(ascii_lowercase + ascii_uppercase):
    priority[l] = i + 1

print(f"Priorities: {priority}")

priority_sum = 0
for line in data.split():
    items = []
    x = int(len(line)/2)
    comp1, comp2 = line[:x], line[x:]
    for item in comp1:
        if item in comp2:
            priority_sum += priority[item]
            break

print(f"The sum of the priorities is {priority_sum}.")

priority_sum = 0
trio = []
for line in data.split():
    trio.append(line)
    if len(trio) == 3:
        for item in trio[0]:
            if item in trio[1] and item in trio[2]:
                priority_sum += priority[item]
                trio = []
                break


print(f"The sum for those item priorities is {priority_sum}.")
