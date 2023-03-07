#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/5
"""
from copy import deepcopy

STOCKS_NUMBER = 9
MAX_STOCK_LEVEL = 7


def create_containers():
    with open("day05_input1.txt", "r") as f:
        graph = (
            f.read()
            .replace("    [", "--- [")
            .replace("]    ", "] ---")
            .replace("]\n", "] ---\n", 1)
        )

    container = [[] for _ in range(STOCKS_NUMBER)]  # list of 9 empty lists
    for line in reversed(graph.split("\n")[:-1]):
        for i, crate in enumerate(line.split()):
            if crate[1] != "-":
                container[i].append(crate[1])  # crate[1] is a character

    show(container)
    return container


def stock_gen(container):
    for i in range(7, -1, -1):
        for stock in container:
            if i < len(stock):
                yield stock[i]
            else:
                yield "-"
        yield "\n"


def show(container):
    for element in stock_gen(container):
        if element == "-":
            print(" --- ", end="")
        elif element == "\n":
            print()  # print new line only
        else:
            print(f" [{element}] ", end="")


class Instruction:
    next = None

    def __init__(self, line: str):
        words = line.split()
        self.how_many = int(words[1])
        self.from_stock = int(words[3]) - 1  # stocks are numbered from 0
        self.to_stock = int(words[5]) - 1  # stocks are numbered from 0


def read_instructions():
    with open("day05_input2.txt", "r") as f:
        before = None
        first_instruction = None
        for line in f.read().split("\n"):
            instruction = Instruction(line)
            if before:
                before.next = instruction
            else:
                first_instruction = instruction
            before = instruction

    return first_instruction


def rearrange(container, instruction):
    while instruction:
        for i in range(instruction.how_many):
            container[instruction.to_stock].append(
                container[instruction.from_stock].pop()
            )
        instruction = instruction.next

    result = "".join(stock[-1] for stock in container)
    print(f"Crate ends up on the top of each stack after rearrangement {result}")


def next_rearrange(container, instruction):
    while instruction:
        stock = container[instruction.from_stock]
        stock_len = len(stock) - instruction.how_many
        container[instruction.to_stock] += stock[stock_len:]
        del stock[stock_len:]
        instruction = instruction.next

    result = "".join(stock[-1] for stock in container)
    print("Crate ends up on the top of each stack after second rearrangement ", result)


def main():
    container = create_containers()
    instructions = read_instructions()
    container_copy = deepcopy(container)

    rearrange(container, instructions)
    next_rearrange(container_copy, instructions)


if __name__ == "__main__":
    main()
