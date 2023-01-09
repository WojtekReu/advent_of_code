#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/18
"""


def read_input() -> list:
    with open("day18.input.txt", "r") as f:
    # with open('day18.test.txt', "r") as f:
        data = f.read()

    cubes = []
    for line in data.split("\n"):
        x, y, z = line.split(",")
        cube = Cube(x, y, z)
        cubes.append(cube)
    return cubes


def show(cubes):
    for cube in cubes:
        print(cube)


def simulate(cubes):
    space = set()
    space_should_be = 0
    for cube in cubes:
        cube.create_surfaces()
        for surface in cube.surfaces:
            space.add(surface)

        space_should_be += 6

    print(f"{space_should_be=}, {len(space)=}")
    surface_sum = 2 * len(space) - space_should_be
    return surface_sum, space


def check_holes(cubes, surfaces):
    min_x = min(cubes, key=lambda c: c.x)
    max_x = max(cubes, key=lambda c: c.x)
    min_y = min(cubes, key=lambda c: c.y)
    max_y = max(cubes, key=lambda c: c.y)
    min_z = min(cubes, key=lambda c: c.z)
    max_z = max(cubes, key=lambda c: c.z)
    # print(f"{min_x.x=}, {max_x.x=}")
    # print(f"{min_y.y=}, {max_y.y=}")
    # print(f"{min_z.z=}, {max_z.z=}")

    air_cubes = []
    for x in range(min_x.x - 1, max_x.x + 2):
        for y in range(min_y.y - 1, max_y.y + 2):
            for z in range(min_z.z - 1, max_z.z + 2):
                c = Cube(x, y, z)
                if c not in cubes:
                    air_cubes.append(c)

    air_cubes_queue = [air_cubes[0]]
    water_cubes = []
    i = 0
    while air_cubes_queue:
        i += 1
        cube = air_cubes_queue.pop()
        water_cubes.append(cube)
        for neigh in cube.get_neighbours():
            if neigh in air_cubes:
                if neigh not in water_cubes:
                    if neigh not in air_cubes_queue:
                        air_cubes_queue.insert(0, neigh)

    surface_sum = 0
    for water_cube in water_cubes:
        water_cube.create_surfaces()
        for surface in water_cube.surfaces:
            if surface in surfaces:
                surface_sum += 1

    print("Air cube: ", len(air_cubes), "water cubes", len(water_cubes))
    return surface_sum


class Cube:
    def __init__(self, x, y, z):
        self.surfaces = {}
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def __repr__(self):
        return f"<{self.x},{self.y},{self.z}>"

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        return False

    def create_surfaces(self):
        self.surfaces = {
            (1, self.x, self.y, self.z),
            (1, self.x + 1, self.y, self.z),
            (2, self.x, self.y, self.z),
            (2, self.x, self.y + 1, self.z),
            (3, self.x, self.y, self.z),
            (3, self.x, self.y, self.z + 1),
        }

    def get_neighbours(self):
        return (
            Cube(self.x + 1, self.y, self.z),
            Cube(self.x - 1, self.y, self.z),
            Cube(self.x, self.y + 1, self.z),
            Cube(self.x, self.y - 1, self.z),
            Cube(self.x, self.y, self.z + 1),
            Cube(self.x, self.y, self.z - 1),
        )


cubes_data = read_input()
# show(cubes_data)
result_sum_surface, surface_data = simulate(cubes_data)
print(f"The surface area of scanned lava droplet is {result_sum_surface}.")

surface_sum_value = check_holes(cubes_data, surface_data)
print(f"The exterior surface area of scanned lava droplet is {surface_sum_value}.")
