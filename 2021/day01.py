#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/1
"""
with open('day01.input.txt', "r") as f:
    data = f.read()

old_depth = 99999999
increase_count = 0

for str_number in data.split():
    depth = int(str_number)
    if old_depth < depth:
        increase_count += 1

    old_depth = depth

print(f"There are {increase_count} measurements that are larger than the previous")

old_depth = 99999999
part_depth1 = 99999
part_depth2 = 99999
increase_count2 = 0

for str_number in data.split():
    part_depth0 = int(str_number)
    depth = part_depth0 + part_depth1 + part_depth2
    if old_depth < depth:
        increase_count2 += 1

    part_depth2 = part_depth1
    part_depth1 = part_depth0
    old_depth = depth

print(f"There are {increase_count2} sums that are larger than the previous sum.")
