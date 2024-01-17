#!/usr/bin/env python3
"""
https://adventofcode.com/2020/day/5
"""
from tools.input import read_input, grid_one

FILENAME_INPUT = "day05.input.txt"
FILENAME_TEST = "day05.test.txt"
ROWS_MAX = 128
COLS_MAX = 8


def calculate(boarding_passes):
    max_seat_id = 0
    seats_missing = set(range(ROWS_MAX * COLS_MAX))
    for boarding_pass in boarding_passes:
        row = int(boarding_pass.replace("F", "0").replace("B", "1")[:7], base=2)
        col = int(boarding_pass.replace("L", "0").replace("R", "1")[-3:], base=2)
        seat_id = row * COLS_MAX + col
        seats_missing.remove(seat_id)
        max_seat_id = max(max_seat_id, seat_id)

    seats_missing = list(sorted(seats_missing))
    your_seat_id = None
    for i, seat_id_before in enumerate(seats_missing, start=2):
        try:
            seat_id = seats_missing[i - 1]
            seat_id_next = seats_missing[i]
        except IndexError:
            continue
        if seat_id_before + 1 != seat_id and seat_id != seat_id_next - 1:
            your_seat_id = seat_id
            break

    return max_seat_id, your_seat_id


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    bp = grid_one(data)
    result1, result2 = calculate(bp)
    print(f"The highest seat ID on a boarding pass is {result1}.")
    print(f"Your seat ID is {result2}.")

    assert result1 == 919
    assert result2 == 642
