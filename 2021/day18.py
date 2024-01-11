#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/18
"""
from copy import deepcopy
from itertools import combinations
from typing import Self

from tools.input import read_input


FILENAME_INPUT = "day18.input.txt"


class SnailFish:
    parent: Self = None
    l: int | Self
    r: int | Self

    def __init__(self, s_list: list[list | int]):
        """
        Change list type `s_list` to type SnailFish or int
        """
        self.create_element("l", s_list[0])
        self.create_element("r", s_list[1])

    def __repr__(self):
        return f"[{self.l},{self.r}]"

    def __add__(self, other):
        snailfish = SnailFish([self, other])
        self.parent = snailfish
        other.parent = snailfish
        while True:
            is_reduced = snailfish.reduce(1)
            # print(snailfish)
            if not is_reduced:
                is_split = snailfish.split()
                if not is_split:
                    break
        return snailfish

    def create_element(self, side: str, el: list | int):
        """
        Create node. Side maybe `l` (left) or `r` (right) node. Element list is changed to
        SnailFish object and parent SnailFish is set. Element int is just set.
        """
        if isinstance(el, list):
            value = SnailFish(el)
            value.parent = self
        else:  # el is int
            value = el
        setattr(self, side, value)

    def split(self) -> bool:
        is_split = False
        if isinstance(self.l, SnailFish):
            is_split = self.l.split()
        elif 9 < self.l:
            self.split_snailfish("l")
            return True
        if is_split:
            return True

        if isinstance(self.r, SnailFish):
            is_split = self.r.split() or is_split
        elif 9 < self.r:
            self.split_snailfish("r")
            return True
        return is_split

    def split_snailfish(self, side):
        el = getattr(self, side)
        i, rest = divmod(el, 2)
        self.create_element(side, [i, i + rest])

    def explode(self):
        self.upgrade_down("l", self.l)
        self.upgrade_down("r", self.r)
        if self.parent.l is self:
            self.parent.l = 0
        elif self.parent.r is self:
            self.parent.r = 0

    def reduce(self, nested: int) -> bool:
        is_exploded = False

        if 4 < nested:
            self.explode()
            return True

        if isinstance(self.l, SnailFish):
            is_exploded = self.l.reduce(nested + 1)
            if is_exploded:
                return True

        if isinstance(self.r, SnailFish):
            is_exploded = self.r.reduce(nested + 1) or is_exploded

        return is_exploded

    def upgrade_down(self, side, value):
        if not self.parent:
            return

        el = getattr(self.parent, side)
        if isinstance(el, SnailFish):
            if el is self:
                self.parent.upgrade_down(side, value)
            else:
                side = "l" if side == "r" else "r"
                el.upgrade_up(side, value)
        else:
            self.parent.add_value(side, value)

    def upgrade_up(self, side, value):
        el = getattr(self, side)
        if isinstance(el, SnailFish):
            el.upgrade_up(side, value)
        else:
            self.add_value(side, value)

    def add_value(self, side, value):
        value += getattr(self, side)  # add existed value for side to new value
        setattr(self, side, value)

    def magnitude(self) -> int:
        """
        magnitude sum is 3 * left + 2 * right, for left and right as snailfish must be calculated
        recurrently.
        """
        magnitude_sum = 3 * (
            self.l.magnitude() if isinstance(self.l, SnailFish) else self.l
        ) + 2 * (self.r.magnitude() if isinstance(self.r, SnailFish) else self.r)
        return magnitude_sum


def prepare(data: str):
    homework = []
    for line in data.split("\n"):
        l = eval(line)
        snailfish = SnailFish(l)
        homework.append(snailfish)
    return homework


def do_homework(numbers_list):
    sum_snailfish = None
    for snailfish in numbers_list:
        if not sum_snailfish:
            sum_snailfish = snailfish
        else:
            sum_snailfish += snailfish

        # print(snailfish)
    # print(sum_snailfish)
    return sum_snailfish


def find_max_magnitude(numbers_list):
    max_magnitude = 0
    for s1, s2 in combinations(numbers_list, 2):
        res = deepcopy(s1) + deepcopy(s2)
        max_magnitude = max(max_magnitude, res.magnitude())
        res = deepcopy(s2) + deepcopy(s1)
        max_magnitude = max(max_magnitude, res.magnitude())

    return max_magnitude


def t(filename) -> str:
    """
    This function is for testing purpose only.
    """
    data = read_input(filename)
    nl = prepare(data)
    return repr(do_homework(nl))


def main(filename):
    data = read_input(filename)
    nl = prepare(data)
    ss = do_homework(nl)
    result1 = ss.magnitude()
    print(f"The magnitude of the final sum is {result1}.")

    nl = prepare(data)
    result2 = find_max_magnitude(nl)
    print(f"The largest magnitude of any sum of two different snailfish numbers is {result2}.")

    assert result1 == 3725
    assert result2 == 4832


def test_reduce():
    assert t("day18.test.1.txt") == "[[[[5,0],[7,4]],[5,5]],[6,6]]"
    assert t("day18.test.2.txt") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    assert t("day18.test.3.txt") == "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"
    assert t("day18.test.4.txt") == "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]"
    assert t("day18.test.5.txt") == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"
    assert t("day18.test.6.txt") == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"
    assert t("day18.test.7.txt") == "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"


if __name__ == "__main__":
    test_reduce()
    main(FILENAME_INPUT)
