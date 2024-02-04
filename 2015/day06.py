#!/usr/bin/env python3
"""
https://adventofcode.com/2015/day/6
real time  0m13,855s
"""
from tools.input import read_input

FILENAME_INPUT = "day06.input.txt"
GRID_RANGE = 1000


def prepare(data):
    instructions = []
    for line in data.split("\n"):
        instruction = []
        if line.startswith("turn on"):
            instruction.append("turn on")
        elif line.startswith("turn off"):
            instruction.append("turn off")
        elif line.startswith("toggle"):
            instruction.append("toggle")
        for word in line.split():
            if "," in word:
                for number in word.split(","):
                    instruction.append(int(number))
        instructions.append(tuple(instruction))

    return instructions


def create_grid():
    return [[0 for _ in range(GRID_RANGE)] for _ in range(GRID_RANGE)]


def lights_on_off(ins_text, light):
    if ins_text == "turn on":
        return 1
    elif ins_text == "turn off":
        return 0
    elif ins_text == "toggle":
        return 0 if light else 1


def brightness(ins_text, light):
    if ins_text == "turn on":
        return light + 1
    elif ins_text == "turn off":
        return light - 1 if light else 0
    elif ins_text == "toggle":
        return light + 2


def follow(ins, grid, instruction_function):
    for y, row in enumerate(grid):
        if ins[2] <= y <= ins[4]:
            for x, light in enumerate(row):
                if ins[1] <= x <= ins[3]:
                    grid[y][x] = instruction_function(ins[0], grid[y][x])


def calculate(instructions, instruction_function) -> int:
    grid = create_grid()
    for instruction in instructions:
        follow(instruction, grid, instruction_function)
    return sum(sum(v) for v in grid)


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    instr = prepare(data)
    result1 = calculate(instr, lights_on_off)
    print(f"There are {result1} lights on.")

    result2 = calculate(instr, brightness)
    print(f"The total brightness value is {result2}.")

    assert result1 == 400410
