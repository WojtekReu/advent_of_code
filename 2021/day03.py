#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/3
"""
with open('day03.input.txt', "r") as f:
    data = f.read()

how_many_1 = [0,0,0,0,0,0,0,0,0,0,0,0]

lines_nr = 500  # half of 1000 lines
max_nr = pow(2, 12) - 1  # 4095

for line in data.split("\n"):
    for nr, bit in enumerate(line):
        if bit == "1":
            how_many_1[nr] += 1

gamma_str = ""

for pos in how_many_1:
    if pos > 500:
        gamma_str = f"{gamma_str}1"
    elif pos < 500:
        gamma_str = f"{gamma_str}0"
    else:
        raise ValueError("Equal number of occurance 0 and 1 is 500")

gamma = int(gamma_str, 2)
epsilon = max_nr - gamma

print(f"Power consumption of submarine is {gamma} * {epsilon} = {gamma * epsilon}")


data2 = [v for v in data.split("\n")]

for pos in range(12):
    counter_1 = 0
    counter_0 = 0
    for line in data2:
        if line[pos] == '0':
            counter_0 += 1
        else:
            counter_1 += 1
    if counter_0 > counter_1:
        search_el = "0"
    else:
        search_el = "1"
    data2 = [v for v in data2 if v[pos] == search_el]

    if len(data2) == 1:
        break

oxygen_gr = int(data2[0], 2)

data2 = [v for v in data.split("\n")]

for pos in range(12):
    counter_1 = 0
    counter_0 = 0
    for line in data2:
        if line[pos] == '0':
            counter_0 += 1
        else:
            counter_1 += 1
    if counter_1 < counter_0:
        search_el = "1"
    else:
        search_el = "0"
    data2 = [v for v in data2 if v[pos] == search_el]

    if len(data2) == 1:
        break

co2_sr = int(data2[0], 2)
print(f"Life support rating is: {oxygen_gr} * {co2_sr} = {oxygen_gr * co2_sr}")
