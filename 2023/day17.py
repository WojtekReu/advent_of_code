#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/17
P1 : real time 0m2,149s
"""
import heapq

FILENAME_TEST = "day17.test.txt"
FILENAME_INPUT = "day17.input.txt"

REVERSED_DIRECTIONS = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E",
}


class Block:
    is_finished: bool = False

    def __init__(self, y, x, heat_loose):
        self.y = y
        self.x = x
        self.heat_loose = int(heat_loose)
        self.adjacents = {}
        self.sum_on_cross = {
            "N": 9999999,
            "W": 9999999,
            "S": 9999999,
            "E": 9999999,
        }

    def __repr__(self):
        return f"<{self.heat_loose}, y={self.y}, x={self.x}>"

    def __le__(self, other):
        return self.sum_on_cross < other.sum_on_cross

    def __gt__(self, other):
        return other.sum_on_cross < self.sum_on_cross

    def set(self, direction, y, x, grid):
        block_next = get_point(y, x, grid)
        if block_next:
            self.adjacents[direction] = block_next

    def join(self, grid):
        self.set("W", self.y, self.x - 1, grid)
        self.set("E", self.y, self.x + 1, grid)
        self.set("N", self.y - 1, self.x, grid)
        self.set("S", self.y + 1, self.x, grid)


class Crucible:
    block: Block
    steps_straight: int = 0
    direction_straight: str = ""
    sum: int = 0

    def __init__(self, block, steps_straight, direction_straight, c_sum, visited):
        self.block = block
        self.steps_straight = steps_straight
        self.direction_straight = direction_straight
        self.sum = c_sum
        self.visited = visited

    def __repr__(self):
        return f"C: {self.block} sum:{self.sum}"

    def __le__(self, other):
        return self.sum < other.sum

    def __gt__(self, other):
        return other.sum < self.sum

    def next_step(self):
        self.visited.append(self.block)
        for direction, block in self.block.adjacents.items():
            if self.is_allowed(direction):
                if self.direction_straight == direction:
                    yield Crucible(
                        block,
                        self.steps_straight + 1,
                        self.direction_straight,
                        self.sum + block.heat_loose,
                        self.visited.copy(),
                    )
                else:
                    if self.sum < block.sum_on_cross[direction]:
                        block.sum_on_cross[direction] = self.sum
                        yield Crucible(
                            block, 0, direction, self.sum + block.heat_loose, self.visited.copy()
                        )

    def is_allowed(self, direction):
        if self.direction_straight == direction:
            if 2 <= self.steps_straight:
                return False
        elif REVERSED_DIRECTIONS[direction] == self.direction_straight:
            return False
        return True


def get_point(y, x, grid):
    if y < 0 or x < 0 or len(grid) - 1 < y or len(grid[0]) - 1 < x:
        return None
    return grid[y][x]


def show(grid, visited):
    for row in grid:
        for b in row:
            if b in visited:
                print(b.heat_loose, end="")
            else:
                print(".", end="")
        print("")


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    grid = [[Block(y, x, c) for x, c in enumerate(line)] for y, line in enumerate(data.split("\n"))]

    for row in grid:
        for b in row:
            b.join(grid)

    return grid


def calculate(grid):
    path_with_min_loses = 9999999

    y_max = len(grid) - 1
    x_max = len(grid[0]) - 1
    bs: Block = grid[0][0]
    bs.sum_on_cross = {
        "N": 0,
        "E": 0,
        "S": 0,
        "W": 0,
    }
    be: Block = grid[y_max][x_max]
    be.is_finished = True

    heap = []
    crucible_start = Crucible(
        block=bs,
        steps_straight=0,
        direction_straight="W",
        c_sum=0,
        visited=[],
    )
    heapq.heappush(heap, crucible_start)

    while heap:
        crucible = heapq.heappop(heap)
        if crucible.block.is_finished:
            if crucible.sum < path_with_min_loses:
                path_with_min_loses = crucible.sum
                blocks_before_for_path = crucible.visited.copy()

        for c_next in crucible.next_step():
            heapq.heappush(heap, c_next)

    print("--------------")
    show(grid, blocks_before_for_path)
    return path_with_min_loses


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    g = prepare(data)
    res1 = calculate(g)
    print(f"The possible least heat loss is {res1}.")
    assert res1 == 870
