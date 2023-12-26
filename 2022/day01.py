#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/1
"""
with open('day01_input.txt', "r") as f:
    data = f.read()

elves = [[]]
for line in data.split("\n"):
    if line == '':
        elves.append([])
    else:
        elves[-1].append(int(line))

max_value = max([sum(calories) for calories in elves])

print(f"Elf carrying most Calories cary {max_value} calories.")

sum_3 = sum(sorted([sum(calories) for calories in elves])[-3:])

print(f"The top three Elves carrying total {sum_3} calories.")
