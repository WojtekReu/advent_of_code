#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/15
real time   10m15,688s
"""
FILENAME = "day15.test.txt"
INITIAL_RISK_LEVEL = 999999


class Position:
    lowest_total_risk = 0
    is_finish = False

    def __init__(self, risk_level):
        self.risk_level = int(risk_level)
        self.neighbors = []
        self.plus_only_neighbors = []

    def __repr__(self):
        return f"<{self.risk_level}>"

    def get_neighbors(self, is_plus_only):
        if is_plus_only:
            return self.plus_only_neighbors
        return self.neighbors


def read_input(filename):
    with open(filename, "r") as f:
        return f.read()


def print_grid(g):
    for row in g:
        for p in row:
            print(p.risk_level, end="")
        print()


def prepare(data, is_larger_cave=False):
    grid = [[Position(val) for val in line] for line in data.split("\n")]
    if is_larger_cave:
        grid_new = []
        for j in range(5):
            for row in grid:
                row_new = []
                for i in range(5):
                    for pos in row:
                        risk_level = sum(divmod(pos.risk_level + j + i, 10))
                        row_new.append(Position(risk_level))
                grid_new.append(row_new)
        grid = grid_new

    start_position = grid[0][0]
    grid[-1][-1].is_finish = True

    y_max = len(grid) - 1
    for y, row in enumerate(grid):
        x_max = len(row) - 1
        for x, pos in enumerate(row):
            if x < x_max:
                pos.neighbors.append(grid[y][x + 1])
                pos.plus_only_neighbors.append(grid[y][x + 1])
            if y < y_max:
                pos.neighbors.append(grid[y + 1][x])
                pos.plus_only_neighbors.append(grid[y + 1][x])
            if 0 < x:
                pos.neighbors.append(grid[y][x - 1])
            if 0 < y:
                pos.neighbors.append(grid[y - 1][x])

    # print_grid(grid)

    return start_position


def simulate(start_position, initial_pf_risk_level=None):
    paths = [start_position]
    # The minimal risk level for finished position.
    if initial_pf_risk_level:
        # slow calculating exactly the lowest total risk level
        pf_risk_level = initial_pf_risk_level
        is_plus_only = False
    else:
        # fast calculating almost the lowest total risk level
        pf_risk_level = INITIAL_RISK_LEVEL
        is_plus_only = True
    c = 0
    try:
        while paths:
            path = paths.pop()
            for next_p in path.get_neighbors(is_plus_only):
                new_risk_level = path.lowest_total_risk + next_p.risk_level
                if pf_risk_level < new_risk_level:
                    continue
                if not next_p.lowest_total_risk or new_risk_level < next_p.lowest_total_risk:
                    if next_p.is_finish:
                        pf_risk_level = new_risk_level
                    else:
                        next_p.lowest_total_risk = new_risk_level
                        paths.append(next_p)
            c += 1
            if c % 10_000_000 == 0:
                print(f"{c} \t Total risk: {pf_risk_level}, paths len: {len(paths)}")
    except KeyboardInterrupt:
        return f"{c} Keyboard Interrupt when calculating lowest total risk: {pf_risk_level}"

    return pf_risk_level


if __name__ == "__main__":
    data = read_input(FILENAME)
    sp = prepare(data)
    total_lowest_risk = simulate(sp, INITIAL_RISK_LEVEL)
    print(f"The total lowest risk level for the small cave is {total_lowest_risk}.")
    sp2 = prepare(data, is_larger_cave=True)
    approximate_value = simulate(sp2)
    print(f"The approximate value: {approximate_value}.")
    sp2 = prepare(data, is_larger_cave=True)
    total_lowest_risk2 = simulate(sp2, approximate_value)
    print(f"The total lowest risk level for the large cave is {total_lowest_risk2}.")
