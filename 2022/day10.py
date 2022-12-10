#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/10
"""

with open('day10_input.txt', "r") as f:
    data = f.read()

commands = []
for line in data.split("\n"):
    words = line.split()
    command_name = words[0]
    value = int(words[1]) if len(words) > 1 else None
    commands.append((command_name, value))

commands = [i for i in reversed(commands)]

commands_len = len(commands)
print("commands len: ", len(commands))

cycles = []

for i in range(commands_len):
    command = commands.pop()
    # print(command)
    if command[0] == 'noop':
        cycles.append(command)
    elif command[0] == 'addx':
        cycles.append(None)
        cycles.append(command)

print("cycles len: ", len(cycles))

interesting_cycles = (20, 60, 100, 140, 180, 220)
sum_of_signal = 0
x = 1
add_value = False
sprite = [['.' for i in range(40)] for j in range(6)]
sprite_row = 0
for nr, cycle in enumerate(cycles):
    if nr in interesting_cycles:
        signal_strength = nr * x
        sum_of_signal += signal_strength
        print(f"{nr=}, {x=}     {signal_strength=}")
    if add_value:
        x += add_value
        add_value = False
    if cycle is None or cycle[0] == 'noop':
        pass
    elif cycle[0] == 'addx':
        add_value = cycle[1]
    sprite_row = nr // 40
    sprite_pos = nr % 40
    a = x - 1
    b = x + 1
    if a <= sprite_pos <= b:
        sprite[sprite_row][sprite_pos] = '#'

print(f"{sum_of_signal=}")

print()
for row in sprite:
    print(''.join(row))
