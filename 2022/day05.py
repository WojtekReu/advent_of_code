#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/5
"""
from copy import deepcopy

with open('day05_input1.txt', "r") as f:
    data = f.read()

graph = data.replace("    [", "--- [").replace("]    ", "] ---").replace("]\n", "] ---\n", 1)

container_tmp = []
for line in reversed(graph.split("\n")):
    container_tmp.append(line)

container_tmp = container_tmp[1:]
container = [[] for i in range(9)]

for line in container_tmp:
    print(line)
    for i, el in enumerate(line.split()):
        if el[1] != "-":
            container[i].append(el[1])

container2 = deepcopy(container)

with open('day05_input2.txt', "r") as f:
    data = f.read()

for line in data.split("\n"):
    lline = line.split()
    how_many = int(lline[1])
    from_c = int(lline[3]) - 1
    to_c = int(lline[5]) - 1
    for i in range(how_many):
        container[to_c].append(container[from_c].pop())

c_str = ""
for stock in container:
    c_str += stock[-1]

print("Crate ends up on the top of each stack after rearrangement ", c_str)


for line in data.split("\n"):
    lline = line.split()
    how_many = int(lline[1])
    from_c = int(lline[3]) - 1
    to_c = int(lline[5]) - 1
    stock = container2[from_c]
    index_c = len(stock) - how_many
    container2[to_c] += stock[index_c:]
    del stock[index_c:]

c_str = ""
for stock in container2:
    c_str += stock[-1]

print("Crate ends up on the top of each stack after second rearrangement ", c_str)
