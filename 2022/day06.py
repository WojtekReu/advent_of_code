#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/6
"""

with open('day06_input.txt', "r") as f:
    data = f.read()


def find_signal(length):
    begin = 0
    end = length
    process = True
    signal = ""

    while process:
        signal = data[begin:end]
        process = False
        for l in signal:
            if signal.count(l) > 1:
                process = True
                break

        begin += 1
        end += 1

        if end == len(data):
            print("NOT FOUND")
            break

    print(f"For {length} long signal you must read {end - 1} characters, signal: {signal}")

find_signal(4)
find_signal(14)
