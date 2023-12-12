#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/12
teal time  for P1   2m0,697
"""
from itertools import product
import re

FILENAME_TEST_1 = "day12.test.1.txt"
FILENAME_INPUT = "day12.input.txt"


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def show(condition_records):
    for r in condition_records:
        print(r)


def prepare(data: str):
    condition_records = []
    for line in data.split("\n"):
        springs_row, condition_record = line.split()
        condition_record = [int(cr) for cr in condition_record.split(",")]
        springs_row = springs_row.replace(".", "-").replace("?", ".")
        condition_records.append((springs_row, condition_record))

    # show(condition_records)
    return condition_records


def get_possible(sr):
    sr_len = len(sr)
    for p in product("#-", repeat=sr_len):
        r = "".join(p)
        yield r


def calculate(condition_records):
    possible = 0
    l = len(condition_records)
    for springs_row, condition_record in condition_records:
        possible_part = 0
        for pos in get_possible(springs_row):
            n_list = [len(s) for s in pos.split("-") if len(s) > 0]
            if n_list == condition_record:
                if re.match(springs_row, pos):
                    # print(condition_record, pos, n_list)
                    possible_part += 1
        possible += possible_part
        l -= 1
        # print(f"\t{l}   {possible_part}         {springs_row}")

    return possible


if __name__ == "__main__":
    data = read_input(FILENAME_TEST_1)
    cr = prepare(data)
    result = calculate(cr)
    print(f"The sum is  {result}.")
    assert result == 7163
