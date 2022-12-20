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
        numbers[i] = nr_before = nr_obj
    return list(reversed(numbers))


class Number:
    nr: int
    next_nr: Self | None = None

    def __init__(self, nr, next_nr):
        self.nr = nr
        self.next_nr = next_nr

    def __repr__(self):
        return f"<{self.nr}>"


def calculate(numbers: list, nr_obj):
    len_numbers = len(numbers)
    while nr_obj:
        if nr_obj.nr == 0:
            nr_obj = nr_obj.next_nr
            continue
        nr_position = numbers.index(nr_obj)
        new_position = nr_position + nr_obj.nr
        if new_position == 0:
            # go to the end list instead of beginning list
            new_position = len_numbers
        new_position = new_position % (len_numbers - 1)
        numbers.remove(nr_obj)
        numbers.insert(new_position, nr_obj)
        nr_obj = nr_obj.next_nr
    return numbers


def get_sum_coordinates(numbers, pos):
    for index_0, nr_obj in enumerate(numbers):
        if nr_obj.nr == 0:
            # found index for Number(0, ...)
            break
    len_numbers = len(numbers)
    sum_coordinates = 0
    print(f"Zero found on position {index_0} in list length {len_numbers}")
    for index_coord in pos:
        new_index = (index_0 + index_coord) % len_numbers
        sum_coordinates += numbers[new_index].nr
        print(new_index, numbers[new_index])

    return sum_coordinates


def calculate_with_key(numbers, decryption_key=1, calculation_count=1):
    for nr_obj in numbers:
        nr_obj.nr *= decryption_key
    first_element = numbers[0]
    for i in range(1, calculation_count + 1):
        numbers = calculate(numbers, first_element)
        # print(f'{i=}')
        # print(numbers)

    positions = [1000, 2000, 3000]
    return get_sum_coordinates(numbers, positions)


DECRYPTION_KEY = 811589153

numbers_data = read_input()

numbers_obj = prepare(numbers_data)
result = calculate_with_key(numbers_obj)
print(f"The grove coordinates is {result}.")

numbers_obj = prepare(numbers_data)
result2 = calculate_with_key(numbers_obj, DECRYPTION_KEY, 10)
print(f"The grove coordinates with key is {result2}.")
