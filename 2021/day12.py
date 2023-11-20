#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/12
real	0m3,242s
"""
FILENAME = "day12.input.txt"

def create_connections(data):
    connections = []
    for row in data.split("\n"):
        n1, n2 = row.split("-")
        if n2 != 'start' and n1 != 'end':
            connections.append((n1, n2))
        if n1 != 'start' and n2 != 'end':
            connections.append((n2, n1))
    return connections


def is_in_path(name, path):
    return name in path

def is_twice_in_path(name, path: list):
    for n in path:
        if path.count(n) == 2 and n.islower() and name in path:
            return True
    return False

def calculate_paths(cons, condition):
    paths = []
    paths_stock = []
    for con in cons:
        if con[0] == 'start':
            paths_stock.append(list(con))

    while paths_stock:
        path = paths_stock.pop()
        for con in cons:
            if path[-1] == con[0]:
                if con[1].islower() and condition(con[1], path):
                    continue
                new_path = path.copy()
                new_path.append(con[1])
                if new_path[-1] == 'end':
                    paths.append(new_path)
                else:
                    paths_stock.append(new_path)

    return len(paths)


def read_input(filename):
    with open(filename, "r") as f:
        return f.read()


if __name__ == "__main__":
    data = read_input(FILENAME)
    connections = create_connections(data)
    paths_count = calculate_paths(connections, is_in_path)
    print(f"There is {paths_count} paths when you can visit small caves at most once.")
    paths_count = calculate_paths(connections, is_twice_in_path)
    print(f"There is {paths_count} paths when you can visit single one small cave twice.")

