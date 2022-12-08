#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/2
"""
with open('day02_input.txt', "r") as f:
    data = f.read()

points = 0
for line in data.split("\n"):
    if line.endswith('X'):
        points += 1
    elif line.endswith('Y'):
        points += 2
    elif line.endswith('Z'):
        points += 3

    if line in ('A Z', 'B X', 'C Y'):
        points += 0
    elif line in ('A X', 'B Y', 'C Z'):
        points += 3
    elif line in ('A Y', 'B Z', 'C X'):
        points += 6

print(f"Result of strategy is {points} points.")

"""
    "A": 1, "Rock"
    "B": 2, "Paper"
    "C": 3, "Scissors"
"""
points = 0
for line in data.split("\n"):
    if line.endswith('X'):
        points += 0
    elif line.endswith('Y'):
        points += 3
    elif line.endswith('Z'):
        points += 6

    if line in ('B X', 'A Y', 'C Z'):
        points += 1
    elif line in ('C X', 'B Y', 'A Z'):
        points += 2
    elif line in ('A X', 'C Y', 'B Z'):
        points += 3
print(f"Total score for is {points} points.")
