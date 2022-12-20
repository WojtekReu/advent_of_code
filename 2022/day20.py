#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/20
"""
from typing import Self


def read_input() -> list:
    with open('day20.input.txt', "r") as f:
    # with open('day20.test.txt', "r") as f:
        data = f.read()

    numbers = []
    for line in data.split("\n"):
        numbers.append(int(line))
    return numbers


def prepare(numbers):
    nr_before = None
    numbers = list(reversed(numbers))
    for i, nr in enumerate(numbers):
        nr_obj = Number(nr, nr_before)
        numbers[i] = nr_obj
        nr_before = nr_obj
    return list(reversed(numbers))


class Number:
    nr: int
    next_nr: Self | None = None

    def __init__(self, nr, next_nr):
        self.nr = nr
        self.next_nr = next_nr

    def __repr__(self):
        return f"<{self.nr}>"


def calculate(numbers: list):
    len_numbers = len(numbers)
    nr_obj = numbers[0]
    i = 0
    while nr_obj:
        nr_position = numbers.index(nr_obj)
        new_position = nr_position + nr_obj.nr
        if new_position == 0:
            new_position = len_numbers
        begins_count = new_position // len_numbers
        new_position = new_position % len_numbers + begins_count
        numbers.remove(nr_obj)
        numbers.insert(new_position, nr_obj)
        nr_obj = nr_obj.next_nr
        i += 1
    return numbers


def get_sum_coordinates(numbers, pos):
    for index_0, nr_obj in enumerate(numbers):
        if nr_obj.nr == 0:
            break
    len_numbers = len(numbers)
    sum_coordinates = 0
    print(f"Zero position: {index_0}")
    for index_coord in pos:
        new_index = (index_0 + index_coord) % len_numbers
        sum_coordinates += numbers[new_index].nr
        print(new_index, numbers[new_index])

    return sum_coordinates


numbers_data = read_input()
numbers_obj = prepare(numbers_data)
# print(numbers_obj)
numbers_obj = calculate(numbers_obj)
positions = [1000, 2000, 3000]
result = get_sum_coordinates(numbers_obj, positions)
print(f"The grove coordinates is {result}.")
