#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/8
"""


def read_input(filename):
    with open(filename, "r") as f:
        raw_data = f.read()

    d_signal = []
    for row in raw_data.split("\n"):
        pattern, output = row.split("|")
        # any digit code is sorted alphabetically, ex. acdfg, abd, ...
        d_signal.append(
            (
                ["".join(sorted(x)) for x in pattern.strip().split()],
                ["".join(sorted(x)) for x in output.strip().split()],
            )
        )
    return d_signal


def calculate_digits(d_signal):
    number = 0
    for row in d_signal:
        for element in row[1]:
            if len(element) in (2, 3, 4, 7):
                number += 1
    return number


def check_7(el, d):
    for x in d[7]:
        if x not in el:
            return False
    return True


def check_4_1(el, val):
    for x in val:
        if x not in el:
            return False
    return True


def sum_all_numbers(d_signal):
    digits_sum = 0
    for row in d_signal:
        digits = {}
        for element in row[0]:
            if len(element) == 2:
                digits[1] = element
            elif len(element) == 3:
                digits[7] = element
            elif len(element) == 4:
                digits[4] = element
            elif len(element) == 7:
                digits[8] = element

        val_4_1 = "".join(filter(lambda x: x not in digits[1], [d for d in digits[4]]))

        for element in row[0]:
            if len(element) == 5:
                if check_7(element, digits):
                    digits[3] = element
                elif check_4_1(element, val_4_1):
                    digits[5] = element
                else:
                    digits[2] = element
            elif len(element) == 6:
                if not check_7(element, digits):
                    digits[6] = element
                elif check_4_1(element, val_4_1):
                    digits[9] = element
                else:
                    digits[0] = element

        number = ""
        for element in row[1]:
            for k, v in digits.items():
                if element == v:
                    number = f"{number}{k}"
                    break

        digits_sum += int(number)

    return digits_sum


if __name__ == "__main__":
    digit_signal = read_input("day08.input.txt")
    result = calculate_digits(digit_signal)
    print(f"Digits appear {result} times.")
    result2 = sum_all_numbers(digit_signal)
    print(f"Sum all number is {result2}.")
