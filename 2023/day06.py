#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/06
"""
FILENAME = "day06.input.txt"
from math import prod


def read_input(filename):
    with open(filename, "r") as f:
        return f.read()


def prepare(data):
    race_time = [int(v) for v in data.split("\n")[0].split(":")[1].split()]
    race_dist = [int(v) for v in data.split("\n")[1].split(":")[1].split()]
    races = [r for r in zip(race_time, race_dist)]
    return races


def one_race(races):
    time = int("".join(str(x[0]) for x in races))
    dist = int("".join(str(x[1]) for x in races))
    return time, dist


def calculate(races):
    records = []
    for rtime, rdist in races:
        record_count = 0
        for load in range(1, rtime):
            time_left = rtime - load
            total_dist = time_left * load
            if rdist < total_dist:
                record_count += 1
                # print(f"{rtime = } \t {load = } {total_dist = }")
        records.append(record_count)
    return prod(records)


def calculate2(rtime, rdist):
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
    t, d = one_race(r)
    result2 = calculate2(t, d)
    print(f"You can beat record on {result2} ways.")
