#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/20
pypy3 real time  0m0,476s
"""
from tools.input import read_input


FILENAME_INPUT = "day20.input.txt"
FILENAME_TEST = "day20.test.txt"
PROCESS_COUNT_P1 = 2
PROCESS_COUNT_P2 = 50


def prepare(data: str) -> tuple[str, list[str]]:
    image_enhancement_algorithm, input_image = data.split("\n\n")
    image = [f"..{line}.." for line in input_image.split("\n")]
    dots = "." * len(image[0])
    image.insert(0, dots)
    image.insert(0, dots)
    image.append(dots)
    image.append(dots)
    return image_enhancement_algorithm, image


def do_ie_algorithm(ie_algorithm: str, image: list[str]) -> list[str]:
    c = "#" if image[0][0] == "." and ie_algorithm[0] == "#" else "."
    row_empty = c * (len(image[0]) + 2)
    image_new = [f"{row_empty}", f"{row_empty}"]
    j_max = len(image[0]) - 1
    for i in range(1, len(image) - 1):
        row_new = f"{c}{c}"
        for j in range(1, j_max):
            adjacent = (
                image[i - 1][j - 1 : j + 2] + image[i][j - 1 : j + 2] + image[i + 1][j - 1 : j + 2]
            )
            ie_index = int(adjacent.replace("#", "1").replace(".", "0"), base=2)
            pixel = ie_algorithm[ie_index]
            row_new = f"{row_new}{pixel}"
        row_new = f"{row_new}{c}{c}"
        image_new.append(row_new)

    image_new.append(f"{row_empty}")
    image_new.append(f"{row_empty}")
    return image_new


def count_light_pixel_sum(image: list[str]) -> int:
    return sum([row.count("#") for row in image])


def show(image: list[str]) -> None:
    for row in image:
        print(row)


def calculate(ie_algorithm: str, image: list[str], process_count: int) -> int:
    for _ in range(process_count):
        image = do_ie_algorithm(ie_algorithm, image)

    # show(image)
    light_pixel_sum = count_light_pixel_sum(image)

    return light_pixel_sum


def main(filename):
    data = read_input(filename)
    iea, im = prepare(data)
    result1 = calculate(iea, im, PROCESS_COUNT_P1)
    print(f"After {PROCESS_COUNT_P1} enhancements, the resulting image has {result1} lit pixels.")

    result2 = calculate(iea, im, PROCESS_COUNT_P2)
    print(f"After {PROCESS_COUNT_P2} enhancements, the resulting image has {result2} lit pixels.")

    assert result1 == 4873
    assert result2 == 16394


if __name__ == "__main__":
    main(FILENAME_INPUT)
