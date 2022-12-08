#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/7
"""

with open('day07_input.txt', "r") as f:
    data = f.read()


class Dirs:
    size = 0
    name = ''
    offset = 100_000
    parent = None

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.childs = []

    def append(self, d):
        self.childs.append(d)

    def go_to(self, dirname):
        for dir_el in self.childs:
            if dir_el.name == dirname:
                return dir_el

    def add_size(self, size):
        self.size += size
        if self.parent:
            self.parent.add_size(size)

    def calculate_size(self, sum_size_with_offset):
        for child in self.childs:
            sum_size_with_offset = child.calculate_size(sum_size_with_offset)
            if child.size < child.offset:
                sum_size_with_offset += child.size
        return sum_size_with_offset

    def get_largest_size(self, largest_size, required_space):
        if required_space < self.size < largest_size:
            largest_size = self.size
        for child in self.childs:
            size = child.get_largest_size(largest_size, required_space)
            if required_space < size < largest_size:
                largest_size = size
        return largest_size


main = Dirs('/', None)
current = main
count_output = False

for line in data.split("\n"):
    # print(line)
    words = line.split()
    if line.startswith("$"):
        count_output = False
    if count_output:
        if words[0] == "dir":
            d = Dirs(words[1], current)
            current.append(d)
        else:
            current.add_size(int(words[0]))

    if line.startswith("$ cd "):
        dirname = words[2]
        if dirname == "/":
            current = main
        elif dirname == "..":
            current = current.parent
        else:
            current = current.go_to(dirname)

    elif line.startswith("$ ls"):
        count_output = True

sum_dirs = main.calculate_size(0)

print(f"Sum of the total size directories under {main.offset} size is {sum_dirs}.")
print(f"{main.size=}")

required_space = main.size + 30_000_000 - 70_000_000

print(f"{required_space=}")  # 3313415

largest_size = main.get_largest_size(main.size, required_space)

print(f"Total size of directory you can delete is {largest_size}.")
