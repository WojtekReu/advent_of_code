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


def get_next_value(history, go_back):
    history_new = [history[i + 1] - history[i] for i in range(len(history) - 1)]
    if any(history_new):
        v_next = get_next_value(history_new, go_back)
        if go_back:
            return history[0] - v_next
        else:
            return history[-1] + v_next
    else:
        return history[-1] + history_new[-1]


def calculate(total_history, go_back=False):
    v_sum = 0
    for history in total_history:
        v = get_next_value(history, go_back)
        v_sum += v
    return v_sum


if __name__ == "__main__":
    data = read_input(FILENAME)
    th = prepare(data)
    result = calculate(th)
    print(f"The sum of extrapolated values in P1 is {result}.")
    assert result == 2075724761

    result = calculate(th, True)
    print(f"The sum of extrapolated values in P2 is {result}.")
    assert result == 1072
