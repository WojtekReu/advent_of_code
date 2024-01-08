#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/12
pypy3 real time for P1  2m5,919s
pypy3 real time for P2  0m8,565s
"""
from functools import lru_cache
from itertools import product
import re

FILENAME_INPUT = "day12.input.txt"
FILENAME_TEST = "day12.test.txt"


@lru_cache(maxsize=1_000_000)
def combinations(symbols, numbers):
    """
    For symbols and numbers check combination of the sequence or subsequence.
    Based on https://github.com/ssobczak/advent-of-code/blob/main/src/2023/python/day_12.py
    """
    symbols = symbols.strip(".")  # the outside dots doesn't have any effect on the result

    if len(numbers) == 0:
        if "#" in symbols:
            return 0
        return 1

    for i, symbol in enumerate(symbols):
        # This loop counts only "#" symbols, for any other symbol this calls another combinations function
        if symbol == ".":
            num = symbols[:i].count("#")
            if num == numbers[0]:
                next_symbols = symbols[i + 1 :]
                next_numbers = numbers[1:]
                result = combinations(next_symbols, next_numbers)
                return result
            else:
                return 0

        if symbol == "#":
            continue

        if symbol == "?":
            # Replace current "?" to "." and "#", then check all combinations for string
            next_symbols1 = symbols[:i] + "#" + symbols[i + 1 :]
            result1 = combinations(next_symbols1, numbers)

            next_symbols2 = symbols[:i] + "." + symbols[i + 1 :]
            result2 = combinations(next_symbols2, numbers)

            result = result1 + result2
            return result

    if len(numbers) == 1 and symbols.count("#") == numbers[0]:
        return 1
    return 0


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def show(condition_records):
    for r in condition_records:
        print(r)


def prepare(data: str, folded=True):
    condition_records = []
    for line in data.split("\n"):
        springs_row, condition_record = line.split()
        if folded:
            springs_row = springs_row
            condition_records.append(
                (
                    springs_row.replace(".", "-").replace("?", "."),
                    [int(cr) for cr in condition_record.split(",")],
                )
            )
        else:
            condition_records.append(
                (
                    f"{springs_row}?{springs_row}?{springs_row}?{springs_row}?{springs_row}",
                    tuple(int(cr) for cr in condition_record.split(",")) * 5,
                )
            )

    # show(condition_records)
    return condition_records


def get_possible(sr):
    for p in product("#-", repeat=len(sr)):
        yield "".join(p)


def calculate(condition_records):
    possible = 0
    l = len(condition_records)
    for springs_row, condition_record in condition_records:
        possible_for_row = 0
        for pos in get_possible(springs_row):
            n_list = [len(s) for s in pos.split("-") if len(s) > 0]
            if n_list == condition_record:
                if re.match(springs_row, pos):
                    possible_for_row += 1
        # print(possible_for_row, springs_row, condition_record)
        possible += possible_for_row
        l -= 1

    return possible


def calculate2(condition_records):
    possible = 0
    for springs_row, condition_record in condition_records:
        possible_for_row = combinations(springs_row, condition_record)
        # print(possible_for_row, springs_row, condition_record)
        possible += possible_for_row

    return possible


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    cr1 = prepare(data)  # For P1 input data are folded
    result1 = calculate(cr1)
    print(f"The sum of possible arrangements for rows on folded list is {result1}.")

    cr2 = prepare(data, folded=False)
    result2 = calculate2(cr2)
    print(f"The sum of possible arrangements for rows on unfolded list is {result2}.")

    assert result1 == 7163
    assert result2 == 17788038834112
