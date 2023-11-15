#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/11
"""

class Octopus:
    flash: bool = False
    energy: int

    def __init__(self, e):
        self.energy = int(e)
        self.neigh = []

    def __repr__(self):
        return f"<O: {self.energy}>"

    def increase_energy(self):
        if self.flash:
            return

        self.energy += 1
        if 9 < self.energy:
            self.flash = True
            self.energy = 0
            for o_neigh in self.neigh:
                o_neigh.increase_energy()

def read_input(filename):
    with open(filename, "r") as f:
        data = f.read()

    grid = []
    for row in data.split('\n'):
        o_row = [Octopus(i) for i in row]
        grid.append(o_row)

    octopuses_list = []
    y_max = len(grid) - 1
    for y, row in enumerate(grid):
        if y == 0:
            y_indexes = (0, 1)
        elif y == y_max:
            y_indexes = (y - 1, y)
        else:
            y_indexes = (y - 1, y, y + 1)

        x_max = len(row) - 1
        for x, o in enumerate(row):
            octopuses_list.append(o)
            if x == 0:
                x_indexes = (0, 1)
            elif x == x_max:
                x_indexes = (x - 1, x)
            else:
                x_indexes = (x - 1, x, x + 1)
            for j in y_indexes:
                for i in x_indexes:
                    if j != y or i != x:
                        o.neigh.append(grid[j][i])

    return octopuses_list

def simulate_flashes(octopuses, step_limit=None):
    total_flash_count = 0
    flash_count = 0
    step = 0

    while flash_count != 100:
        flash_count = 0
        step += 1

        # increase energy
        for o in octopuses:
            o.increase_energy()
        # count flashes
        for o in octopuses:
            if o.flash:
                o.flash = False
                flash_count += 1
                total_flash_count += 1

        if step_limit and step_limit == step:
            break

    return total_flash_count, step


if __name__ == "__main__":
    o_list = read_input("day11.input.txt")
    flashes, _ = simulate_flashes(o_list, 100)
    print(f"After 100 steps there are {flashes} flashes.")

    _, steps = simulate_flashes(o_list)
    print(f"After {steps + 100} steps all flashes are synchronized.")
