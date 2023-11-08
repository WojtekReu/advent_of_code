#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/7
"""
from statistics import median


def calculate_fuel_for_best_position(positions: list) -> tuple:
    position = int(median(positions))
    total = sum(abs(x - position) for x in positions)

    return position, total


def fuel_consumption(x1: int, x2: int) -> int:
    distance = abs(x2 - x1)
    return int(distance * (distance + 1) / 2)


def calculate_fuel_for_increasing_consumption(positions: list) -> tuple:
    min_position = min(positions)
    max_position = max(positions)
    total_before = 999999999
    for position in range(min_position, max_position):
        total = sum(fuel_consumption(x, position) for x in positions)
        if total_before < total:
            return position - 1, total_before
        total_before = total

    return max_position, total_before


if __name__ == "__main__":
    with open("day07.input.txt", "r") as f:
        data = [int(x) for x in f.read().split(",")]

    optimal_position, fuel = calculate_fuel_for_best_position(data)
    print(f"They must spend {fuel} to align to {optimal_position} position.")

    position2, fuel2 = calculate_fuel_for_increasing_consumption(data)
    print(f"They must spend {fuel2} to align to {position2} position for increasing consumption.")
