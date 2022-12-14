#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/12
"""
from string import ascii_lowercase
from typing import Self


class Square:
    visited = False
    is_finish = False
    is_path_to_finish = False
    up: Self
    right: Self
    down: Self
    left: Self
    parent: Self
    step: int

    def __init__(self, letter, row, col):
        self.neighborhood = []
        self.letter = letter
        self.row = row
        self.col = col
        self.height = ascii_lowercase.index(self.letter)

    def __repr__(self):
        return f"<{self.letter} ({self.row},{self.col})>"

    def can_move(self, square: Self):
        if square.height - self.height <= 1:
            return True
        return False

    def next(self, sq_queue):
        for el in self.neighborhood:
            if not el.visited:
                el.step = self.step + 1
                el.visited = True
                sq_queue.insert(0, el)
                el.parent = self

    def draw_path_to_beginning(self):
        self.is_path_to_finish = True
        if hasattr(self, 'parent'):
            self.parent.draw_path_to_beginning()

    def get_letter(self):
        return '·' if self.is_path_to_finish else self.letter


def read_input():
    with open('day12_input.txt', "r") as f:
        data = f.read()

    b_coords = e_coords = None
    squares = []

    for row, line in enumerate(data.split("\n")):
        # print(line)
        square_row = []
        squares.append(square_row)
        for col, letter in enumerate(line):
            if letter == 'S':
                b_coords = row, col
                letter = 'a'
            elif letter == 'E':
                e_coords = row, col
                letter = 'z'
            square_row.append(Square(letter, row, col))
    return squares, b_coords, e_coords


def join_squares(squares):
    grid_rows_len = len(squares)
    grid_cols_len = len(squares[0])

    for row, square_row in enumerate(squares):
        # print(square_row)
        for col, square in enumerate(square_row):
            if 0 <= row - 1:
                up = squares[row - 1][col]
                if square.can_move(up):
                    square.neighborhood.append(up)
                    square.up = up
            if col + 1 < grid_cols_len:
                right = squares[row][col + 1]
                if square.can_move(right):
                    square.neighborhood.append(right)
                    square.right = right
            if row + 1 < grid_rows_len:
                down = squares[row + 1][col]
                if square.can_move(down):
                    square.neighborhood.append(down)
                    square.down = down
            if 0 <= col - 1:
                left = squares[row][col - 1]
                if square.can_move(left):
                    square.neighborhood.append(left)
                    square.left = left


def find_way(square):
    square.step = 0
    square.visited = True
    queue_squares = [square]
    while queue_squares:
        square = queue_squares.pop()
        square.next(queue_squares)
        if square.is_finish:
            return square.step


def clear_squares(squares):
    for square_row in squares:
        for square in square_row:
            square.visited = False


def find_shortest_hiking(squares):
    min_path_length = 100000
    for square_row in squares:
        for square in square_row:
            if square.letter == 'a':
                clear_squares(squares)
                path_length = find_way(square)
                if path_length:
                    min_path_length = min(min_path_length, path_length)
    return min_path_length


def draw(squares, square_end):
    square_end.draw_path_to_beginning()
    picture = ''
    for row in squares:
        for square in row:
            picture += square.get_letter()
        picture += "\n"
    picture += "\n"
    return picture


squares_data, beginning_coords, end_coords = read_input()

start = squares_data[beginning_coords[0]][beginning_coords[1]]
end = squares_data[end_coords[0]][end_coords[1]]
end.is_finish = True

join_squares(squares_data)

steps_number = find_way(start)
pic = draw(squares_data, end)
print(pic)
print(f"The fewest steps required to move to the location is {steps_number}")

shortest_hiking = find_shortest_hiking(squares_data)
print(f"shortest hiking: {shortest_hiking}")
