#!/usr/bin/env python3
"""
https://adventofcode.com/2020/day/04
"""
from tools.input import read_input

FILENAME_INPUT = "day04.input.txt"
FILENAME_TEST = "day04.test.txt"
PASSPORTS_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}


def is_valid_extend(passport):
    try:
        if not (
            (1920 <= int(passport["byr"]) <= 2002)
            and (2010 <= int(passport["iyr"]) <= 2020)
            and (2020 <= int(passport["eyr"]) <= 2030)
        ):
            return False
    except ValueError:
        return False

    if not passport["hgt"].endswith("cm") and not passport["hgt"].endswith("in"):
        return False

    try:
        if passport["hgt"].endswith("cm") and not (150 <= int(passport["hgt"][:-2]) <= 193):
            return False
        if passport["hgt"].endswith("in") and not (59 <= int(passport["hgt"][:-2]) <= 76):
            return False
    except ValueError:
        return False

    if passport["hcl"][0] != "#" or len(passport["hcl"]) != 7:
        return False

    for c in passport["hcl"][1:]:
        if c not in "0123456789abcdef":
            return False

    if passport["ecl"] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return False

    if len(passport["pid"]) != 9 or not passport["pid"].isnumeric():
        return False

    return True


def calculate(passports):
    validate_fields = PASSPORTS_FIELDS.copy()
    validate_fields.remove("cid")
    valid_count = valid_extend_count = 0
    for passport in passports:
        for field in validate_fields:
            if field not in passport:
                break
        else:
            valid_count += 1
            if is_valid_extend(passport):
                valid_extend_count += 1
    return valid_count, valid_extend_count


def prepare_passports(data):
    passports = []
    for line in data.split("\n\n"):
        passport = {}
        passports.append(passport)
        for name_set in line.split():
            k, v = name_set.split(":")
            passport[k] = v
    return passports


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    p = prepare_passports(data)
    result1, result2 = calculate(p)
    print(f"{result1} passports are valid in my batch file.")
    print(f"For extended rules {result2} passports are valid in my batch file.")

    assert result1 == 228
    assert result2 == 175
