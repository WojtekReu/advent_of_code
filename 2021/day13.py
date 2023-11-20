#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/13
"""
FILENAME = "day13.input.txt"


def read_input(filename):
    with open(filename, "r") as f:
        return f.read()


def prepare_data(data):
    dots = []
    folds = []
    for line in data.split("\n"):
        if line:
            if line[0].isdigit():
                x, y = line.split(",")
                dots.append((int(x), int(y)))
            else:
                axis = 0 if line[11] == "x" else 1
                pos = line.split("=")[1]
                folds.append((axis, int(pos)))

    return dots, folds


def print_code(dots):
    max_x = max(dots, key=lambda d: d[0])[0] + 1
    max_y = max(dots, key=lambda d: d[1])[1] + 1

    display = []
    for j in range(max_y):
        display.append(["."] * max_x)

    for x, y in dots:
        display[y][x] = "#"

    for row in display:
        for col in row:
            print(col, end="")
        print("")


def do_folding(dots, folds):
    dots_count_after_first_folding = None
    for axis, fold in folds:
        base = 2 * fold
        new_dots = []
        for dot in dots:
            if dot[axis] == fold:
                raise ValueError(f"Error: Dot {dot} can't be on axis {axis}.")
            pos = base - dot[axis] if fold < dot[axis] else dot[axis]
            if axis == 0:  # x
                new_dots.append((pos, dot[1]))
            else:
                new_dots.append((dot[0], pos))

        if dots_count_after_first_folding is None:
            dots_count_after_first_folding = len(set(new_dots))
            print(
                f"After completing the first fold instruction there is {dots_count_after_first_folding} dots."
            )

        dots = new_dots

    print_code(dots)


if __name__ == "__main__":
    data = read_input(FILENAME)
    d, f = prepare_data(data)
    do_folding(d, f)
