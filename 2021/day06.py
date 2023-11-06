#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/6
"""
from collections import deque

DAYS_1 = 80
DAYS_2 = 256


def run(lanternfish, days) -> int:
    for day in range(days):
        value = lanternfish.popleft()
        lanternfish[6] += value  # 6 internal timer
        lanternfish.append(value)  # 8 internal timer

    return sum(lanternfish)


if __name__ == "__main__":
    lanternfish = deque([0 for i in range(9)])  # internal timers: 0 - 8

    with open("day06.input.txt", "r") as f:
        data = f.read().split(",")

    for internal_timer_value in data:
        # index position is "internal timer" value
        lanternfish[int(internal_timer_value)] += 1

    fish_count = run(lanternfish, DAYS_1)
    print(f"There is {fish_count} after {DAYS_1} days.")

    fish_count = run(lanternfish, DAYS_2 - DAYS_1)
    print(f"There is {fish_count} after {DAYS_2} days.")
