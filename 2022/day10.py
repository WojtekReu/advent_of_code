#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/10
"""

with open('day10_input.txt', "r") as f:
# with open('temp.txt', "r") as f:
    data = f.read()

commands = []
for line in data.split("\n"):
    words = line.split()
    command = words[0]
    value = int(words[1]) if len(words) > 1 else None
    commands.append((command, value))

commands = [i for i in reversed(commands)]
LAST_CYCLE = 220

cycles = []

commands_len = len(commands)
print("commands len: ", len(commands))

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
for nr, cycle in enumerate(cycles):
    if nr in interesting_cycles:
        signal_strength = nr * x
        sum_of_signal += signal_strength
        print(f"{cycle=}, {nr=}, {x=}     {signal_strength=}")
    if add_value:
        x += add_value
        add_value = False
    if cycle is None or cycle[0] == 'noop':
        pass
    elif cycle[0] == 'addx':
        add_value = cycle[1]

print(f"{sum_of_signal=}")
