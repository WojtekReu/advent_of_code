#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/21
pypy3 real time  0m1,975s
"""
from functools import lru_cache
from itertools import cycle, product
from typing import Any

from tools.input import read_input


FILENAME_INPUT = "day21.input.txt"
FILENAME_TEST = "day21.test.txt"
BOARD_MAX = 10
ROLLS = 3
WIN_A = 1000  # in 1 task, player win when gets at least 1000 scores
WIN_B = 21  # in 2 task, player win when gets at least 21 scores
DICE_RANGE = range(1, 101)


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

        return bool(WIN_A <= self.points)


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
    die = Die(DICE_RANGE)
    while True:
        player = next(players)
        if player.roll(die):
            break

    player = next(players)  # player who didn't win

    return player.points * die.count


def move(position: int, rolls: tuple[int, int, int]) -> int:
    new_position = (position + sum(rolls)) % BOARD_MAX
    return new_position if new_position else BOARD_MAX


@lru_cache(maxsize=15_000)
def calc_universes(
    p1_points: int, p2_points: int, p1_position: int, p2_position: int
) -> tuple[int, int]:
    p1_wins = p2_wins = 0
    for p1_rolls in product((1, 2, 3), repeat=3):
        p1_new_position = move(p1_position, p1_rolls)
        p1_new_points = p1_points + p1_new_position
        if WIN_B <= p1_new_points:
            p1_wins += 1
            continue
        for p2_rolls in product((1, 2, 3), repeat=3):
            p2_new_position = move(p2_position, p2_rolls)
            p2_new_points = p2_points + p2_new_position
            if WIN_B <= p2_new_points:
                p2_wins += 1
                continue
            p1_wins_new, p2_wind_new = calc_universes(
                p1_new_points, p2_new_points, p1_new_position, p2_new_position
            )
            p1_wins += p1_wins_new
            p2_wins += p2_wind_new

    return p1_wins, p2_wins


def calculate2(players: Any) -> tuple[int, int]:
    player1 = next(players)
    player2 = next(players)
    return calc_universes(player1.points, player2.points, player1.position, player2.position)


def main(filename):
    data = read_input(filename)
    ps = prepare(data)
    result1 = calculate(ps)
    print(
        f"If you multiply the score of the losing player by the number of times the die was "
        f"rolled during the game you get {result1}."
    )

    ps = prepare(data)
    result2 = calculate2(ps)
    print(
        f"Player 1 wins in {result2[0]} universes, while player 2 wins in {result2[1]} universes. "
        f"Player {'2' if result2[0] < result2[0] else '1'} wins in more universes."
    )

    assert result1 == 605070
    assert max(result2) == 218433063958910


if __name__ == "__main__":
    main(FILENAME_INPUT)
