#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/9
"""

FILENAME = "day09.input.txt"


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    total_history = [[int(n) for n in l.split()] for l in data.split("\n")]
    return total_history


def get_next_value(history):
    v0 = None
    history_new = []
    for v in history:
        if v0 is not None:
            history_new.append(v - v0)
        v0 = v
    if any(history_new):
        v_next = get_next_value(history_new)
        return history[-1] + v_next
    else:
        return history[-1] + history_new[-1]

def calculate(total_history):
    v_sum = 0
    for history in total_history:
        # print(history)
        v = get_next_value(history)
        # print(v)
        v_sum += v
    return v_sum



if __name__ == "__main__":
    data = read_input(FILENAME)
    th = prepare(data)
    result = calculate(th)
    print(f"res 1 :{result}")
    # assert result == 11199999
