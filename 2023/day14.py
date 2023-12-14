#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/14
"""
import numpy

FILENAME_TEST = "day14.test.txt"
FILENAME_INPUT = "day14.input.txt"


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    matrix = [[c for c in line] for line in data.split()]
    np_matrix = numpy.array(matrix)
    mt = np_matrix.transpose()
    # print(mt)
    return mt

def move_to_bound(row, x):
    if x == 0:
        return
    for i in range(x -1, -1, -1):
        if row[i] == 'O' or row[i] == '#':
            if i + 1 != x:
                row[i + 1] = 'O'
                row[x] = "."
            return
        elif i == 0:
            row[i] = "O"
            row[x] = "."
            return


def calculate(matrix):
    max_val = len(matrix[0])
    for y, row in enumerate(matrix):
        for x, el in enumerate(row):
            if el == 'O':
                move_to_bound(row, x)

    # print(matrix)

    sum_c = 0
    for row in matrix:
        for i, el in enumerate(row):
            if el == 'O':
                sum_c += (max_val - i)


    return sum_c


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    mt = prepare(data)
    res1 = calculate(mt)
    print(f"The total load is {res1}.")
    assert res1 == 108918
