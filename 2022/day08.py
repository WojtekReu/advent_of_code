#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/8
"""

with open('day08_input.txt', "r") as f:
        data = f.read()


class Tree:
    is_hidden = True

    def __init__(self, height):
        self.height = int(height)

    def is_visible(self):
        self.is_hidden = False

    def calculate_scenic(self, row, col):
        for i in range(1, row + 1):
            tree = grid[row - i][col]
            if self.height <= tree.height:
                highest_index_up = i
                break
        else:
            highest_index_up = i

        # Right
        my_range = max_col - col
        for i in range(1, my_range):
            tree = grid[row][col + i]
            if self.height <= tree.height:
                highest_index_right = i
                break
        else:
            highest_index_right = i

        # down
        my_range = max_row - row
        for i in range(1, my_range):
            tree = grid[row + i][col]
            if self.height <= tree.height:
                highest_index_down = i
                break
        else:
            highest_index_down = i

        # left
        for i in range(1, col + 1):
            tree = grid[row][col - i]
            if self.height <= tree.height:
                highest_index_left = i
                break
        else:
            highest_index_left = i

        scenic_i = highest_index_up * highest_index_right * highest_index_down * highest_index_left
        # print(f"{self.height} {row=} {col=}  ", highest_index_up, highest_index_right, highest_index_down, highest_index_left, ' = ', scenic_i)
        return scenic_i


def find_visible_from_site(site_grid):
    max_height = []
    for row, row_trees in enumerate(site_grid):
        for col, tree in enumerate(row_trees):
            if row == 0:
                max_height.append(tree.height)
                tree.is_visible()
            else:
                if max_height[col] < tree.height:
                    tree.is_visible()
                    max_height[col] = tree.height


grid = []
trees_all_number = 0
for i, line in enumerate(data.split()):
    # print(line)
    line_grid = []
    grid.append(line_grid)
    for nr in line:
        line_grid.append(Tree(nr))
        trees_all_number += 1

find_visible_from_site(grid)
# from bottom
find_visible_from_site(reversed(grid))

transfered_grid = []
for row, row_trees in enumerate(grid):
    for col, tree in enumerate(row_trees):
        if len(transfered_grid) < col + 1:
            transfered_grid.append([])
        dest_row = transfered_grid[col]
        dest_row.append(tree)

# from left
find_visible_from_site(transfered_grid)
# from right
find_visible_from_site(reversed(transfered_grid))

hidden_trees_number = 0
for row_trees in grid:
    for tree in row_trees:
        if tree.is_hidden:
            hidden_trees_number += 1

print(f"Number of all trees: {trees_all_number}")
visible = trees_all_number - hidden_trees_number
print(f"Number of hidden trees: {hidden_trees_number} and visible trees: {visible}")

max_row = len(grid)
max_col = len(grid[0])
print(f"{max_row=}    {max_col=}")

max_scenic = 0
for row, row_trees in enumerate(grid):
    for col, tree in enumerate(row_trees):
        if col == 0 or row == 0 or col == max_col - 1 or row == max_row - 1:
            continue
        scenic = tree.calculate_scenic(row, col)
        max_scenic = max(max_scenic, scenic)

print(f"Max scenic: {max_scenic}")
