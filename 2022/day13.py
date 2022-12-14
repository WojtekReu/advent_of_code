#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/13
"""

DIVIDER_LEFT = [[2]]
DIVIDER_RIGHT = [[6]]


def read_input():
    with open('day13_input.txt', "r") as f:
        data = f.read()

    packages = []
    left = None
    right = None
    for nr, line in enumerate(data.split("\n")):
        if line:
            if left is None:
                left = eval(line)
            else:
                right = eval(line)
        if left is not None and right is not None:
            index = len(packages) + 1
            packages.append((left, right))
            left = right = None
    return packages


def compare(left, right):
    if isinstance(left, int):
        if isinstance(right, int):
            if left < right:
                return 'left'
            elif right < left:
                return 'right'
        elif isinstance(right, list):
            return compare([left], right)
    elif isinstance(left, list):
        if isinstance(right, int):
            return compare(left, [right])
        elif isinstance(right, list):
            for i, i_left in enumerate(left):
                if i < len(right):
                    i_right = right[i]
                    result = compare(i_left, i_right)
                    if result is not None:
                        return result
                else:
                    return 'right'
            if len(left) < len(right):
                return 'left'
            elif len(right) < len(left):
                return 'right'


def count_correct_packages(packages):
    right_order = 0
    for p_index, package in enumerate(packages, start=1):
        left = package[0]
        right = package[1]
        result = compare(left, right)
        if result == 'left':
            right_order += p_index
    return right_order


def change_structure(packages):
    new_packages = []
    for package in packages:
        new_packages.append(package[0])
        new_packages.append(package[1])

    new_packages.append(DIVIDER_LEFT)
    new_packages.append(DIVIDER_RIGHT)
    return new_packages


def sort_packages(packages):
    sort_again = True
    while sort_again:
        sort_again = False
        for i in range(len(packages) - 1):
            left = packages[i]
            right = packages[i+1]
            result = compare(left, right)
            if result == 'right':
                packages[i] = right
                packages[i+1] = left
                sort_again = True
                break


def find_dividers(packages):
    index_divider_left = index_divider_right = 0
    for i, package in enumerate(packages, start=1):
        # print(i, package)
        if package == DIVIDER_LEFT:
            index_divider_left = i
        if package == DIVIDER_RIGHT:
            index_divider_right = i

    return index_divider_left * index_divider_right


packages_data = read_input()
print(f"Pairs number: {len(packages_data)}")

sum_indices = count_correct_packages(packages_data)
print(f"The sum of the indices right order packages is: {sum_indices}")

packages_data = change_structure(packages_data)
sort_packages(packages_data)
decoder_key = find_dividers(packages_data)

print(f"The decoder key for the distress signal is: {decoder_key}")
