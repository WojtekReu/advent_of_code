#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/06
"""
FILENAME = "day06.input.txt"
from math import prod, sqrt


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str) -> list[tuple]:
    race_time = [int(v) for v in data.split("\n")[0].split(":")[1].split()]
    race_dist = [int(v) for v in data.split("\n")[1].split(":")[1].split()]
    races = [r for r in zip(race_time, race_dist)]
    return races


def input_for_one_race(races: list[tuple]) -> tuple[int, int]:
    time = int("".join(str(x[0]) for x in races))
    dist = int("".join(str(x[1]) for x in races))
    return time, dist


def fast_calculation(races: list[tuple]) -> int:
    """
    The rounding beaten_records some times is different by 1 from real beaten records value.
    """
    records_product = 1
    for rtime, rdist in races:
        beaten_records = count_beaten_records(rtime, rdist)
        records_product *= int(beaten_records)
    return records_product


def count_beaten_records(time: int, record: int) -> float:
    """
    Solve the inequality: record < x * time - x**2
    """
    # x1 = int((time - sqrt(pow(time, 2) - 4 * record)) / 2)
    # x2 = int((time + sqrt(pow(time, 2) - 4 * record)) / 2)
    # return x2 - x1
    return sqrt(pow(time, 2) - 4 * record)


def calculate(races: list[tuple]) -> int:
    """
    Very slow calculation
    """
    records = []
    for rtime, rdist in races:
        record_count = 0
        for load in range(1, rtime):
            time_left = rtime - load
            total_dist = time_left * load
            if rdist < total_dist:
                record_count += 1
        records.append(record_count)
    return prod(records)


def calculate2(rtime: int, rdist: int) -> int:
    """
    Slow calculation
    """
    not_record = 0
    for load in range(rtime):
        time_left = rtime - load
        total_dist = time_left * load

        if rdist < total_dist:
            not_record = load - 1
            break  # from this load value race beats the record

    # count from max race time to 1
    for load in range(rtime, 1, -1):
        time_left = rtime - load
        total_dist = time_left * load

        not_record += 1
        if rdist < total_dist:
            not_record -= 1
            break  # from this load value race beats the record
    return rtime - not_record


if __name__ == "__main__":
    data = read_input(FILENAME)
    r = prepare(data)
    result = calculate(r)
    print(f"Multiply the numbers of ways you could beat the record is: {result}.")
    t, d = input_for_one_race(r)
    result2 = count_beaten_records(t, d)
    print(f"For time={t} you can beat distance record={d} on {int(result2)} ways.")
