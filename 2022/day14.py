#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/14
"""
from typing import Self

SOURCE_COORD = (500, 0)


def read_input() -> list:
    with open('day14_input.txt', "r") as f:
        data = f.read()

    rock_paths = []
    for nr, line in enumerate(data.split("\n")):
        # print(line)
        rock_path = []
        rock_paths.append(rock_path)
        for word in line.split():
            if "," in word:
                coords = word.split(",")
                rock_path.append((int(coords[0]), int(coords[1])))
    return rock_paths


def create_grid(rock_paths):
    x_list = [coords[0] for row in rock_paths for coords in row]
    x_min = min(x_list)
    x_max = max(x_list)
    y_list = [coords[1] for row in rock_paths for coords in row]
    y_min = min(y_list)
    y_min = min(0, y_min)
    y_max = max(y_list)

    print(f"{x_min=} -> {x_max},   {y_min=} -> {y_max}")
    grid = []
    for y in range(y_min, y_max + 1):
        row = []
        grid.append(row)
        for x in range(x_min, x_max + 1):
            if x == SOURCE_COORD[0] and y == SOURCE_COORD[1]:
                p = Point(x, y, '+')
            else:
                p = Point(x, y)
            row.append(p)
    return grid


def join_neighbors(grid):
    row_max = len(grid)
    pos_max = len(grid[0])

    for row_nr, row in enumerate(grid):
        for pos_nr, point in enumerate(row):
            if pos_nr < pos_max - 1:
                point.right = grid[row_nr][pos_nr+1]
            if row_nr < row_max - 1:
                point.down = grid[row_nr+1][pos_nr]
            if 0 < pos_nr:
                point.left = grid[row_nr][pos_nr-1]
    return grid


def create_rock_paths(rock_paths, grid):
    x_min = grid[0][0].x
    for rock_path in rock_paths:
        corner_a = None
        for corner_b in rock_path:
            if corner_a:
                pos1 = corner_a[0] - x_min
                pos2 = corner_b[0] - x_min
                if pos1 == pos2:  # x
                    if corner_a[1] < corner_b[1]:
                        start, stop = corner_a[1], corner_b[1]
                    else:
                        start, stop = corner_b[1], corner_a[1]
                    for y_coord in range(start, stop + 1):
                        grid[y_coord][pos1].material = '#'
                else:
                    if pos1 < pos2:
                        start, stop = pos1, pos2
                    else:
                        start, stop = pos2, pos1
                    for y_coord in range(start, stop + 1):
                        grid[corner_a[1]][y_coord].material = '#'

            corner_a = corner_b

    return grid


def display(grid):
    for row in grid:
        row_str = ''
        for point in row:
            row_str += point.material
        print(row_str)
    print()


def simulate(grid):
    source = None
    y_end = len(grid) - 1
    for point in grid[0]:
        if point.material == '+':
            source = point
            break

    sand = Sand(source)
    stuck_sand_nr = 0

    def condition_1():
        return sand.position.y < y_end

    def condition_2():
        return sand.simulation_go_on

    condition = condition_1 if grid[-1][0].material == '.' else condition_2

    while condition():
        sand.move()
        if sand.is_stuck:
            stuck_sand_nr += 1
            sand = Sand(source)

    return stuck_sand_nr


def extend_grid(grid):
    extend_floor = 2
    y_min = 0
    y_max = len(grid) - 1 + extend_floor
    x_min = SOURCE_COORD[0] - y_max - 2
    x_max = SOURCE_COORD[0] + y_max + 2
    old_grid_x_min = grid[0][0].x
    old_grid_x_max = grid[0][-1].x
    old_grid_y_min = grid[0][0].y
    old_grid_y_max = grid[-1][0].y

    grid2 = []
    for y in range(y_min, y_max + 1):
        row = []
        grid2.append(row)
        for x in range(x_min, x_max + 1):
            if old_grid_y_min <= y <= old_grid_y_max and old_grid_x_min <= x <= old_grid_x_max:
                point = grid[y][x-old_grid_x_min]
                if point.material == 'o':
                    point.material = '.'

            else:
                point = Point(x, y)

            if point.y == y_max:
                point.material = '#'

            row.append(point)

    return grid2


class Point:
    material: str
    x: int
    y: int
    down: Self
    right: Self
    left: Self

    def __init__(self, x: int, y: int, material: str = '.'):
        self.x = x
        self.y = y
        self.material = material

    def __repr__(self):
        return f"<{self.x},{self.y} {self.material}>"

    def is_air(self):
        if self.material == '.':
            return True
        return False


class Sand:
    position: Point
    is_stuck: bool = False
    simulation_go_on = True

    def __init__(self, point):
        if point.material == 'o':
            self.simulation_go_on = False
        else:
            self.position = point

    def move(self):
        if self.position.down.is_air():
            self.position = self.position.down
        elif self.position.down.left.is_air():
            self.position = self.position.down.left
        elif self.position.down.right.is_air():
            self.position = self.position.down.right
        else:
            self.stuck()

    def stuck(self):
        self.is_stuck = True
        self.position.material = 'o'


rock_paths_data = read_input()
grid_data = create_grid(rock_paths_data)
grid_data = join_neighbors(grid_data)
grid_data = create_rock_paths(rock_paths_data, grid_data)
# display(grid_data)
sand_number = simulate(grid_data)
display(grid_data)

print(f"{sand_number} units of sand come to rest before sand starts flowing into the abyss below.")

grid_data = extend_grid(grid_data)
grid_data = join_neighbors(grid_data)
sand_number = simulate(grid_data)
display(grid_data)

print(f"{sand_number} units of sand come to rest.")
