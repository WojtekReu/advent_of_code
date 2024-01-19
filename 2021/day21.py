#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/21
pypy3 real time for P1  0m0,093s
"""
from itertools import cycle
from typing import Any

from tools.input import read_input


FILENAME_INPUT = "day21.input.txt"
FILENAME_TEST = "day21.test.txt"
BOARD_MAX = 10
ROLLS = 3
WIN_P1 = 1000
WIN_P2 = 21


class Player:
    nr: str
    points: int = 0

    def __init__(self, nr, v):
        self.nr = nr
        self.position = int(v)

    def __repr__(self):
        return f"Player {self.nr}: on {self.position} pos, {self.points} points"

    def roll(self, die):
        for _ in range(ROLLS):
            new_position = (self.position + next(die)) % BOARD_MAX
            self.position = new_position if new_position else BOARD_MAX
        self.points += self.position

        return bool(WIN_P1 <= self.points)


class Die(cycle):  # dice
    count: int = 0

    def __next__(self):
        self.count += 1
        return super().__next__()


def prepare(data: str) -> Any:
    players_list = []
    for line in data.split("\n"):
        words = line.split()
        players_list.append(Player(words[1], words[-1]))
    return cycle(players_list)


def calculate(players: Any) -> int:
    die = Die(range(1, 101))
    while True:
        player = next(players)
        if player.roll(die):
            break

    player = next(players)  # player who didn't win

    return player.points * die.count


def main(filename):
    data = read_input(filename)
    ps = prepare(data)
    result1 = calculate(ps)
    print(
        f"If you multiply the score of the losing player by the number of times the die was "
        f"rolled during the game you get {result1}."
    )

    assert result1 == 605070


if __name__ == "__main__":
    main(FILENAME_INPUT)
