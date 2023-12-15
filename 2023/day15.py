#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/15
"""
FILENAME_TEST = "day15.test.txt"
FILENAME_INPUT = "day15.input.txt"


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    seq = data.split(",")
    return seq


def get_label(k: str) -> str:
    if "-" in k:
        return k.replace("-", "")
    return k.split("=")[0]


def get_focusing_power(k: str) -> int:
    return int(k.split("=")[1])


def get_hash(label: str) -> int:
    current_value = 0
    for c in label:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    return current_value


def calculate(seq: list) -> tuple[int, list]:
    seq_sum = 0
    lenses = []
    for k in seq:
        seq_sum += get_hash(k)
        lenses.append((k, get_hash(get_label(k))))
    return seq_sum, lenses


def calculate2(lenses: list) -> int:
    boxes = [[] for _ in range(256)]
    for lens, box_id in lenses:
        box = boxes[box_id]
        label = get_label(lens)
        if "-" in lens:
            box[:] = [l for l in box if l[0] != label]
        elif "=" in lens:
            exists = False
            for l in box:
                if l[0] == label:
                    l[1] = get_focusing_power(lens)
                    exists = True

            if not exists:
                box.append([label, get_focusing_power(lens)])

    total_focusing_power = 0
    for i, box in enumerate(boxes, start=1):
        for j, slot in enumerate(box, start=1):
            total_focusing_power += i * j * slot[1]

    return total_focusing_power


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    d = prepare(data)
    res1, l = calculate(d)
    print(f"The sum of the result is {res1}.")
    assert res1 == 504036

    res2 = calculate2(l)
    print(f"For the resulting lens configuration focusing power is {res2}.")
    assert res2 == 295719
