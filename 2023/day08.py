#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/8
"""
from itertools import cycle

FILENAME = "day08.input.txt"


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    instructions = [int(i) for i in data.split("\n")[0].replace("L", "0").replace("R", "1")]
    network = {}
    for line in data.split("\n")[2:]:
        k = line[:3]
        l = line[7:10]
        r = line[12:15]
        network[k] = (l, r)
    return instructions, network


def calculate(instructions, network):
    i_int = cycle(instructions)
    count = 0
    pos = "AAA"
    while pos != "ZZZ":
        next_i = next(i_int)
        pos = network[pos][next_i]
        count += 1
    return count


if __name__ == "__main__":
    data = read_input(FILENAME)
    i, n = prepare(data)
    result = calculate(i, n)
    print(f"Res : {result}.")
    assert result == 17141
