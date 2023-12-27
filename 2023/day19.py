#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/19
real time 0m0,088s
"""
from collections import namedtuple
from copy import deepcopy
from typing import Callable, Self
from math import prod

FILENAME_TEST = "day19.test.txt"
FILENAME_INPUT = "day19.input.txt"


RatingRange = namedtuple("RatingRange", ["min", "max"])


class Condition:
    char: str = ""
    rating_name: str = ""
    value: [int] = None
    condition: Callable
    is_true: Self | str
    is_false: Self | str

    def __init__(self, destination):
        self.destination = destination

    def __repr__(self):
        if self.value:
            return f" {self.rating_name}{self.char}{self.value}:{self.destination} "
        else:
            return f" {self.destination} "

    def set(self, *args):
        self.rating_name = args[0]
        self.value = int(args[1])

    def set_le_condition(self, *args):
        self.set(*args)
        self.char = "<"
        self.condition = lambda x: x < self.value

    def set_ge_condition(self, *args):
        self.set(*args)
        self.char = ">"
        self.condition = lambda x: x > self.value

    def calc(self, rating: dict):
        rating_value = rating[self.rating_name]
        if self.condition(rating_value):
            if isinstance(self.is_true, Condition):
                return self.is_true.calc(rating)
            return self.is_true

        else:
            if isinstance(self.is_false, Condition):
                return self.is_false.calc(rating)
            return self.is_false

    def calc_accepted(self, rating):
        return prod([rr.max - rr.min + 1 for rr in rating.values()])

    def check_condition(self, condition, rating: dict):
        if isinstance(condition, Condition):
            return condition.calc_range(rating)
        elif condition == "A":
            return self.calc_accepted(rating)
        return 0

    def calc_range(self, rating: dict):
        rating_range = rating[self.rating_name]
        new_rating = deepcopy(rating)
        if self.char == "<":
            # (1, 2005) a < 2006
            new_rating[self.rating_name] = RatingRange(rating_range.min, self.value - 1)
            rating[self.rating_name] = RatingRange(self.value, rating_range.max)
        elif self.char == ">":
            # (2091, 4000) m > 2090
            rating[self.rating_name] = RatingRange(rating_range.min, self.value)
            new_rating[self.rating_name] = RatingRange(self.value + 1, rating_range.max)

        ratings_sum = self.check_condition(self.is_true, new_rating)
        ratings_sum += self.check_condition(self.is_false, rating)
        return ratings_sum


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    workflows = {}
    ratings = []
    first_part = True
    for line in data.split("\n"):
        if not line:
            first_part = False
            continue
        if first_part:
            name, conditions = prepare_workflows(line)
            workflows[name] = conditions
        else:
            ratings.append(prepare_ratings(line))

    for workflow in workflows.values():
        for i, condition in enumerate(workflow):
            if isinstance(condition, Condition):
                if condition.destination in ("A", "R"):
                    condition.is_true = condition.destination
                else:
                    condition.is_true = workflows[condition.destination][0]

                false_condition = workflow[i + 1]

                if isinstance(false_condition, Condition):
                    condition.is_false = false_condition
                elif false_condition in ("A", "R"):
                    condition.is_false = false_condition
                else:
                    condition.is_false = workflows[false_condition][0]

    return workflows, ratings


def prepare_workflows(line):
    workflow = []
    name, rest = line.split("{")
    for word in rest.strip("}").split(","):
        if ":" in word:
            word2, condition_dest = word.split(":")
            condition = Condition(condition_dest)
            if "<" in word2:
                condition.set_le_condition(*word2.split("<"))  # rating_name, value
            else:
                condition.set_ge_condition(*word2.split(">"))
        else:
            condition = word
        workflow.append(condition)

    return name, workflow


def prepare_ratings(line):
    return {word[0]: int(word[2:]) for word in line.strip("{}").split(",")}


def calculate(workflows, ratings):
    total_sum = 0
    start_condition = workflows["in"][0]

    for rating in ratings:
        res = start_condition.calc(rating)
        if res == "A":
            part = sum(rating.values())
            total_sum += part

    return total_sum


def calculate2(workflows):
    start_condition = workflows["in"][0]

    rating = {
        "x": RatingRange(1, 4000),
        "m": RatingRange(1, 4000),
        "a": RatingRange(1, 4000),
        "s": RatingRange(1, 4000),
    }

    res = start_condition.calc_range(rating)

    return res


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    w, r = prepare(data)
    res1 = calculate(w, r)
    print(f"The sum of the all accepted ratings is {res1}.")
    assert res1 == 446517

    res2 = calculate2(w)
    print(f"The sum of the result is {res2}.")
    assert res2 == 130090458884662
