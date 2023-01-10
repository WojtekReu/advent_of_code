#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/25
"""


def read_input():
    with open('day25.input.txt', "r") as f:
    # with open('day25.test.txt', "r") as f:
        data = f.read()

    numbers = []
    for row_nr, line in enumerate(data.split("\n")):
        numbers.append(Snafu(line.strip()))
    return numbers


class Snafu:
    numbers: list

    def __init__(self, nr_str):
        self.numbers = []
        for char in reversed(nr_str):
            self.numbers.append(char)

    def __repr__(self):
        return ''.join(reversed(self.numbers))

    @property
    def decimal(self) -> int:
        number = 0
        for i, char in enumerate(self.numbers):
            match char:
                case '=':
                    nr = -2
                case '-':
                    nr = -1
                case '0':
                    nr = 0
                case '1':
                    nr = 1
                case '2':
                    nr = 2
            number += pow(5, i) * nr

        return number


def to_snafu(number: int) -> str:
    snafu_list = []

    while number:
        remainder = number % 5
        number = number // 5
        match remainder:
            case 0:
                fu = '0'
            case 1:
                fu = '1'
            case 2:
                fu = '2'
            case 3:
                fu = '='
                number += 1
            case 4:
                fu = '-'
                number += 1
        snafu_list.append(fu)
    return ''.join(reversed(snafu_list))


numbers_data = read_input()
decimal_sum = 0
for snafu in numbers_data:
    # print(f"{to_snafu(snafu.decimal)} \t {snafu} \t {snafu.decimal} ")
    decimal_sum += snafu.decimal

snafu_sum = to_snafu(decimal_sum)

print(f"The sum in decimal {decimal_sum} snafu {snafu_sum}")
