#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/8
"""
from itertools import cycle
import math

FILENAME = "day08.input.txt"


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    first_line = data.split("\n")[0].replace("L", "0").replace("R", "1")
    instructions = [int(i) for i in first_line]  # Left is 0 and right is 1
    network = {}
    for line in data.split("\n")[2:]:
        k = line[:3]
        l = line[7:10]
        r = line[12:15]
        network[k] = (l, r)
    return instructions, network


def calculate(instructions, network):
    instruction = cycle(instructions)
    count = 0
    pos = "AAA"
    while pos != "ZZZ":
        next_i = next(instruction)
        pos = network[pos][next_i]
        count += 1
    return count


def is_pos_list_end(pos_list, results_list, count):
    elements_to_remove = []
    for node in pos_list:
        if node.endswith("Z"):
            elements_to_remove.append(node)
            results_list.append(count)

    for el in elements_to_remove:
        pos_list.remove(el)

    return bool(pos_list)


def calculate2(instructions, network):
    instruction = cycle(instructions)
    count = 0
    pos_list = [k for k in network.keys() if k.endswith("A")]
    results_list = []
    while is_pos_list_end(pos_list, results_list, count):
        next_i = next(instruction)
        for i, pos in enumerate(pos_list):
            pos_list[i] = network[pos][next_i]
        count += 1
    return math.lcm(*results_list)


if __name__ == "__main__":
    data = read_input(FILENAME)
    i, n = prepare(data)
    result = calculate(i, n)
    print(f"AAA required {result} steps to reach ZZZ.")
    assert result == 17141

    result2 = calculate2(i, n)
    print(f"After {result2} steps all A nodes reach Z.")
    assert result2 == 10818234074807
