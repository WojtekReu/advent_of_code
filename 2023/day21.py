#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/21
pypy3 real time  0m3,272s
"""
from collections import deque, namedtuple, defaultdict, Counter

FILENAME_TEST = "day21.test.txt"
FILENAME_INPUT = "day21.input.txt"

MAX_STEPS_TEST = 6
MAX_STEPS_INPUT_P1 = 64
MAX_STEPS_INPUT_P2 = 26501365

Platform = namedtuple("Platform", ["dy", "dx", "point"])


class Point:
    grid: list
    visited = defaultdict(int)

    def __init__(self, y, x, c):
        self.y = y
        self.x = x
        self.c = c
        self.adjacent: list[Platform] = []
        self.steps = set()
        self.v1 = set()

    def __repr__(self):
        return f"<{self.y},{self.x} {self.c}>"

    def add_adjacent(self, p, y_max: int, x_max: int):
        if p.c != "#":
            if self.x == 0 and 1 < p.x:
                platform = Platform(0, -1, p)
            elif self.x == x_max and p.x == 0:
                platform = Platform(0, 1, p)
            elif self.y == 0 and 1 < p.y:
                platform = Platform(-1, 0, p)
            elif self.y == y_max and p.y == 0:
                platform = Platform(1, 0, p)
            else:
                platform = Platform(0, 0, p)

            self.adjacent.append(platform)


class Gardener:
    available_coords_org: set[str]
    available_platforms: dict[str, set]

    def __init__(self, platform_y, platform_x, point, step):
        self.platform_y: int = platform_y
        self.platform_x: int = platform_x
        self.point: Point = point
        self.step = step

    def __repr__(self):
        return f"G: p({self.platform_y},{self.platform_x}) y={self.point.y}, x={self.point.x}, {self.step} "

    def go(self, max_steps):
        if self.step == max_steps:
            return

        for platform in self.point.adjacent:
            if platform.dx or platform.dy:
                if (
                    platform.dx > 0 > self.platform_x  # dx = 1    x < 0
                    or platform.dx < 0 < self.platform_x  # dx = -1   0 < x
                    or platform.dy > 0 > self.platform_y  # dy = 1   y < 0
                    or platform.dy < 0 < self.platform_y  # dy = -1   0 < y
                ):
                    continue

                platform_new_y = self.platform_y + platform.dy
                platform_new_x = self.platform_x + platform.dx

                try:
                    available_points = self.available_platforms[
                        f"{platform_new_y},{platform_new_x}"
                    ]
                except KeyError:
                    available_points = self.available_coords_org.copy()
                    self.available_platforms[
                        f"{platform_new_y},{platform_new_x}"
                    ] = available_points
            else:
                available_points = self.available_platforms[f"{self.platform_y},{self.platform_x}"]

            try:
                available_points.remove(f"{platform.point.y},{platform.point.x}")
            except KeyError:
                continue
            yield Gardener(
                self.platform_y + platform.dy,
                self.platform_x + platform.dx,
                platform.point,
                self.step + 1,
            )

    def is_even(self, shift) -> bool:
        if (self.step + shift) % 2:  # shift is 0 for odd or 1 for even max_step_number
            self.check_on_grid()
            return True
        return False

    def check_on_grid(self):
        self.point.visited[f"{self.platform_y},{self.platform_x}"] += 1
        self.point.v1.add(f"{self.platform_y},{self.platform_x}")


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    grid = [[Point(y, x, c) for x, c in enumerate(line)] for y, line in enumerate(data.split("\n"))]
    Point.grid = grid

    y_max = len(grid) - 1
    x_max = len(grid[0]) - 1
    available_coords = set()
    for row in grid:
        for p in row:
            p.add_adjacent(grid[p.y][p.x - 1], y_max, x_max)
            if p.x < x_max:
                p.add_adjacent(grid[p.y][p.x + 1], y_max, x_max)
            else:
                p.add_adjacent(grid[p.y][0], y_max, x_max)

            p.add_adjacent(grid[p.y - 1][p.x], y_max, x_max)
            if p.y < y_max:
                p.add_adjacent(grid[p.y + 1][p.x], y_max, x_max)
            else:
                p.add_adjacent(grid[0][p.x], y_max, x_max)

            if p.c == "S":
                point_start: Point = p
                point_start.steps.add("0,0")
                point_start.visited["0,0"] = 1
            if p.c != "#":
                available_coords.add(f"{p.y},{p.x}")

    return point_start, available_coords, grid


def show(grid, max_steps):
    n = 2
    xy_len = (n + 1) * 131
    xy_0 = -n * 131

    count_star = 1
    output = ""
    for y in range(xy_0, xy_len):
        line = ""
        for x in range(xy_0, xy_len):
            platform_y, p_y = divmod(y, 131)
            platform_x, p_x = divmod(x, 131)
            p = grid[p_y][p_x]
            platform = f"{platform_y},{platform_x}"
            if platform in p.v1:
                count_star += 1
                line += "*"
            else:
                line += p.c
        output = f"{output}{line}\n"

    print(output)
    print(f"for {max_steps}: {count_star = }")


def calculate(point_start, available_coords, max_steps):
    shift = 0 if max_steps % 2 else 1
    Gardener.available_coords_org = available_coords
    Gardener.available_platforms = {"0,0": available_coords.copy()}
    Gardener.available_platforms["0,0"].remove(f"{point_start.y},{point_start.x}")

    points_count = shift  # for even starts from 1 but for odd starts from 0
    g_queue = deque()
    g_queue.append(Gardener(0, 0, point_start, 0))

    while g_queue:
        gardener = g_queue.popleft()
        for gardener_next in gardener.go(max_steps):
            g_queue.append(gardener_next)
            if gardener_next.is_even(shift):
                points_count += 1

    return points_count


def calculate_for_grid(point_start, n):  # n = 202300
    k = sum([i * 8 for i in range(n // 2)])
    l = pow(n, 2)
    m = n - 1
    p = pow(n - 1, 2)
    v = point_start.visited
    # for a, b in v.items():
    #     print(a, b)
    # for a, b in Counter([x for x in v.values()]).items():
    #     print(f" {b}*{a} ", end="")
    # print()
    if n % 2:
        total = (
            l * v["0,0"]
            + p * v["0,1"]
            + m * (v["-1,-2"] + v["1,-2"] + v["-1,2"] + v["1,2"])
            + v["0,-3"]
            + v["0,3"]
            + v["-3,0"]
            + v["3,0"]
            + n * (v["-1,-3"] + v["1,-3"] + v["-1,3"] + v["1,3"])
        )
    else:
        total = (
            v["0,0"]
            + l * v["0,1"]
            + k * v["1,1"]
            + m * (v["-1,-3"] + v["1,-3"] + v["-1,3"] + v["1,3"])
            + v["0,-4"]
            + v["0,4"]
            + v["-4,0"]
            + v["4,0"]
            + n * (v["-2,-3"] + v["2,-3"] + v["-2,3"] + v["2,3"])
            - 1
        )
    return total


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    ps, ac, g = prepare(data)
    res1 = calculate(ps, ac, MAX_STEPS_INPUT_P1)
    print(f"In exactly {MAX_STEPS_INPUT_P1} steps the Elf could reach {res1} garden plots.")
    assert res1 == 3740

    ps, ac, g = prepare(data)
    n = (MAX_STEPS_INPUT_P2 - 65) // 131
    if n % 2:
        even_steps = 3 * 131 + 65
    else:
        even_steps = 4 * 131 + 65
    calculate(ps, ac, even_steps)

    res2 = calculate_for_grid(ps, n)
    print(f"In exactly {MAX_STEPS_INPUT_P2} steps the Elf could reach {res2 = } garden plots.")
    assert res2 == 620962518745459
