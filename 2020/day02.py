#!/usr/bin/env python3
"""
https://adventofcode.com/2020/day/02
"""

FILENAME_INPUT = "day02.input.txt"


class PasswordPolicy:
    def __init__(self, words):
        self.min, self.max = map(int, words[0].split("-"))
        self.letter = words[1].strip(":")
        self.password = words[2]

    def __repr__(self):
        return f"{self.min}-{self.max} {self.letter}: {self.password}"

    def sled_rental_policy(self) -> bool:
        return self.min <= self.password.count(self.letter) <= self.max

    def letter_from_password(self, index):
        try:
            return self.password[index - 1]
        except IndexError:
            return ""

    def official_toboggan_corporate_policy(self) -> bool:
        letter1 = self.letter_from_password(self.min)
        letter2 = self.letter_from_password(self.max)
        return (letter1 == self.letter or letter2 == self.letter) and letter1 != letter2

    def policy(self, is_otcp: bool) -> bool:
        return self.official_toboggan_corporate_policy() if is_otcp else self.sled_rental_policy()


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str) -> list[PasswordPolicy]:
    return [PasswordPolicy(line.split()) for line in data.split("\n")]


def calculate(password_policies: list[PasswordPolicy], is_otcp=False) -> int:
    return sum(1 for pp in password_policies if pp.policy(is_otcp))


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    pps = prepare(data)
    result1 = calculate(pps)
    print(f"For sled rental policy {result1} passwords are valid.")

    result2 = calculate(pps, True)
    print(f"For the Official Toboggan Corporate Policy {result2} passwords are valid.")

    assert result1 == 622
    assert result2 == 263
