#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/02
"""
import re

FILENAME = "day02.input.txt"


def read_input(filename):
    with open(filename, "r") as f:
        return f.read()


def calculate(data):
    game_ids = set()
    game_limit = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    for line in data.split("\n"):
        words = [word.replace(",", "").replace(";", "") for word in line.split()]
        game_id = int(words[1].replace(":", ""))

        is_possible = False
        for subset in line.split(";"):
            words = [word.replace(",", "") for word in subset.split()]

            game = {
                "red": 0,
                "green": 0,
                "blue": 0,
            }
            for nr, word in enumerate(words):
                if word.isalpha() and word != "Game":
                    game[word] = int(words[nr - 1])

            if (
                game.get("red", 0) <= game_limit["red"]
                and game.get("green") <= game_limit["green"]
                and game.get("blue") <= game_limit["blue"]
            ):
                is_possible = True
            else:
                is_possible = False
                break

        if is_possible:
            game_ids.add(game_id)

    return sum(game_ids)


def calculate2(data):
    games_cubs_nr_sum = 0
    for line in data.split("\n"):
        game_max = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for subset in line.split(";"):
            words = [word.replace(",", "") for word in subset.split()]

            for nr, word in enumerate(words):
                if word.isalpha() and word != "Game":
                    cubes_nr = int(words[nr - 1])
                    game_max[word] = max(game_max[word], cubes_nr)

        my_val = game_max["red"] * game_max["green"] * game_max["blue"]
        games_cubs_nr_sum += my_val

    return games_cubs_nr_sum


if __name__ == "__main__":
    data = read_input(FILENAME)
    result = calculate(data)
    print(f"The sum of the IDs of those of games is {result}.")

    result2 = calculate2(data)
    print(f"The sum of the power of these sets is {result2}.")
