#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/25
real time  2m55,779s
"""
from networkx import minimum_cut, DiGraph, NetworkXUnbounded


FILENAME_TEST = "day25.test.txt"
FILENAME_INPUT = "day25.input.txt"


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    connections = []
    for line in data.split("\n"):
        name, name_list = line.split(":")
        for name2 in name_list.split():
            connections.append((name, name2))

    return connections


def calculate(connections):
    graph = DiGraph()

    for conn in connections:
        graph.add_edge(conn[0], conn[1], capacity=1.0)
        graph.add_edge(conn[1], conn[0], capacity=1.0)

    minimum_cut_value = 99999.0
    for conn in connections:
        try:
            cut_value, partition = minimum_cut(graph, conn[1], conn[0])
            if cut_value < minimum_cut_value:
                minimum_cut_value = cut_value
                reachable, non_reachable = partition

        except NetworkXUnbounded as e:
            print(f"Error: {e}")

    # print(f"{minimum_cut_value = }")
    reachable_len = len(reachable)
    not_reachable_len = len(non_reachable)

    return reachable_len * not_reachable_len


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    c = prepare(data)

    res = calculate(c)
    print(f"If you multiply the size of these two groups together you get {res}.")
    assert res == 600369
