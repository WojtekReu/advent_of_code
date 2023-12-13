#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/13
real time  0m0,380s
"""
import numpy

FILENAME_TEST = "day13.test.txt"
FILENAME_INPUT = "day13.input.txt"


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def show(mirrors):
    for i, m in enumerate(mirrors, start=1):
        print(f"-----------------{i}---------------------")
        for r in m:
            print("".join(r))
    print("---------------  END MIRRORS -----------------------")


def prepare(data: str):
    mirrors = [[]]
    for line in data.split("\n"):
        if not line:
            mirrors.append([])
        else:
            mirrors[-1].append([c for c in line])
    mirrors = [numpy.array(m) for m in mirrors]
    # show(mirrors)
    return mirrors


def mirror_find(mirror_list, skip_r=0):
    # join rows to strings
    mirror = ["".join(row) for row in mirror_list]

    for i in range(len(mirror) - 1):
        if mirror[i] == mirror[i + 1]:
            if i + 1 != skip_r:
                r = i + 1
                part1 = list(reversed(mirror[:r]))
                part2 = mirror[r:]
                m_len = len([x for x in zip(part1, part2) if x[0] == x[1]])
                has_edge = r == m_len or r + m_len == len(mirror)
                if has_edge:
                    return r


def clean_mirror_orientation(mirror, is_transposed=False):
    smudges = set()

    for i, part1 in enumerate(mirror):
        for j, part2 in enumerate(mirror):
            if i < j:
                indexes = []
                for k, el in enumerate(zip(part1, part2)):
                    if el[0] != el[1]:
                        indexes.append(k)
                if len(indexes) == 1:
                    pos = indexes[0]
                    if is_transposed:
                        smudges.add(tuple(sorted(((pos, i), (pos, j)), key=lambda x: x[1])))
                    else:
                        smudges.add(tuple(sorted(((i, pos), (j, pos)), key=lambda x: x[0])))
    return smudges


def clean_mirror(mirror):
    positions = clean_mirror_orientation(mirror)
    positions.update(clean_mirror_orientation(mirror.transpose(), True))

    for position in positions:
        a, b = position
        if mirror[a[0]][a[1]] == "#":
            mirror[b[0]][b[1]] = "#"
            yield mirror
            mirror[b[0]][b[1]] = "."
            mirror[a[0]][a[1]] = "."
            yield mirror
            mirror[a[0]][a[1]] = "#"
        else:
            mirror[b[0]][b[1]] = "."
            yield mirror
            mirror[b[0]][b[1]] = "#"
            mirror[a[0]][a[1]] = "#"
            yield mirror
            mirror[a[0]][a[1]] = "."


def calculate(mirrors: list):
    reflections_sum_p1 = 0
    reflections_sum_p2 = 0

    for mirror in mirrors:
        r1 = mirror_find(mirror)
        if r1:
            reflections_sum_p1 += r1 * 100
            r2 = 0
        else:
            r2 = mirror_find(mirror.transpose())
            reflections_sum_p1 += r2
            r1 = 0
        skip_r2, skip_r1 = r2, r1

        for m2 in clean_mirror(mirror):
            r1 = mirror_find(m2, skip_r1)
            if r1:
                reflections_sum_p2 += r1 * 100
                break
            r2 = mirror_find(m2.transpose(), skip_r2)
            if r2:
                reflections_sum_p2 += r2
                break

    return reflections_sum_p1, reflections_sum_p2


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    ms = prepare(data)
    res1, res2 = calculate(ms)
    print(f"The sum of the reflections is {res1}.")
    print(f"The sum of the reflections after cleaning the smudges is {res2}.")
    assert res1 == 36015
    assert res2 == 35335
