#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/14
"""
FILENAME = "day14.input.txt"
STEPS1 = 10
STEPS2 = 40


def read_input(filename):
    with open(filename, "r") as f:
        return f.read()


def prepare(data):
    letters = set()
    template = []
    l_before = None
    for l in data.split("\n")[0]:
        letters.add(l)
        if l_before:
            template.append(f"{l_before}{l}")
        l_before = l

    pairs = {}
    for line in data.split("\n")[2:]:
        pair_old, _, letter = line.split()
        letters.add(letter)
        pairs[pair_old] = (f"{pair_old[0]}{letter}", f"{letter}{pair_old[1]}")

    return template, pairs, letters


def simulate(template, pairs):
    for i in range(10):
        template_new = []
        for pair in template:
            template_new += pairs[pair]

        template = template_new
    return template


def quantity(polymer, letters):
    q = {l: 0 for l in letters}
    polymer_str = polymer[0][0] + "".join(p[1] for p in polymer)
    for l in letters:
        q[l] = polymer_str.count(l)

    l_max = max(q, key=q.get)
    l_min = min(q, key=q.get)
    return l_max, q[l_max], l_min, q[l_min]


def simulate_advanced(template, pairs, letters):
    pp = {p: 0 for p in pairs}  # polymer pairs
    for pair in template:
        pp[pair] += 1

    for i in range(40):
        pp_new = {p: 0 for p in pairs}
        for pair in pp.keys():
            a, b = pairs[pair]
            pp_new[a] += pp[pair]
            pp_new[b] += pp[pair]

        pp = pp_new

    letters_dict = {l: 0 for l in letters}
    letters_dict[template[0][0]] += 1
    for pair, nr in pp.items():
        l = pair[1]
        letters_dict[l] += nr

    l_max = max(letters_dict, key=letters_dict.get)
    l_min = min(letters_dict, key=letters_dict.get)
    return l_max, letters_dict[l_max], l_min, letters_dict[l_min]


if __name__ == "__main__":
    data = read_input(FILENAME)
    t, p, l = prepare(data)
    pol = simulate(t, p)
    letter_max, v_max, letter_min, v_min = quantity(pol, l)
    print(
        f"After {STEPS1} max occurrence has {letter_max}: {v_max}; min {letter_min} {v_min}; quantity: {v_max - v_min}"
    )
    letter_max, v_max, letter_min, v_min = simulate_advanced(t, p, l)
    print(
        f"After {STEPS2} max occurrence has {letter_max}: {v_max}; min {letter_min} {v_min}; quantity: {v_max - v_min}"
    )
