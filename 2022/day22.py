#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/22
"""

L_RANGES = {
    "A": (0, 1, 51, 101, "J"),
    "B": (0, 1, 101, 151, "I"),
    "C": (1, 51, 151, 152, "F"),
    "D": (51, 52, 102, 151, "E"),
    "X": (51, 52, 101, 102, "X"),
    "E": (52, 101, 101, 102, "D"),
    "F": (101, 151, 101, 102, "C"),
    "G": (151, 152, 52, 101, "H"),
    "Y": (151, 152, 51, 52, "Y"),
    "H": (152, 201, 51, 52, "G"),
    "I": (201, 202, 1, 51, "B"),
    "J": (151, 201, 0, 1, "A"),
    "K": (101, 151, 0, 1, "N"),
    "L": (100, 101, 1, 50, "M"),
    "Z": (100, 101, 50, 51, "Z"),
    "M": (51, 100, 50, 51, "L"),
    "N": (1, 51, 50, 51, "K"),
}


def read_input():
    with open("day22.input.txt", "r") as f:
        # with open("day22.test.txt", "r") as f:
        data = f.read()

    data1, data2 = data.split("\n\n", maxsplit=1)

    force_field = []
    for line in data1.split("\n"):
        row = [" "]  # first element is right border
        force_field.append(row)
        for element in line:
            row.append(element)
        row.append(" ")  # last element is left border

    len_ff_row = len(force_field[0])

    for row in force_field:
        while len(row) < len_ff_row:
            row.append(" ")

    border = [" "] * len_ff_row
    force_field.insert(0, border.copy())
    force_field.append(border.copy())

    # print(f"{len_ff_row=}   {len(force_field)=}")

    moves = []
    nr_str = ""
    for letter in data2:
        if letter == "L" or letter == "R":
            if nr_str:
                moves.append(int(nr_str))
                nr_str = ""
            moves.append(letter)
        else:
            nr_str += letter
    if nr_str:
        moves.append(int(nr_str))
    return force_field, moves


def form_cube(force_field):
    # (row0, row1, col0, col1)
    l_ranges = {
        "A": (0, 1, 51, 101),
        "B": (0, 1, 101, 151),
        "C": (1, 51, 151, 152),
        "D": (51, 52, 102, 151),
        "X": (51, 52, 101, 102),
        "E": (52, 101, 101, 102),
        "F": (101, 151, 101, 102),
        "G": (151, 152, 52, 101),
        "Y": (151, 152, 51, 52),
        "H": (152, 201, 51, 52),
        "I": (201, 202, 1, 51),
        "J": (151, 201, 0, 1),
        "K": (101, 151, 0, 1),
        "L": (100, 101, 1, 50),
        "Z": (100, 101, 50, 51),
        "M": (51, 100, 50, 51),
        "N": (1, 51, 50, 51),
    }
    for letter, pos in l_ranges.items():
        for y in range(pos[0], pos[1]):
            for x in range(pos[2], pos[3]):
                if force_field[y][x] != " ":
                    raise ValueError(
                        f"Trying overwrite '{force_field[y][x]}' by {letter} on {x=},{y=}"
                    )
                force_field[y][x] = letter


def show(force_field):
    for row in force_field:
        row_str = "".join(row)
        print(row_str)


def simulate(force_field, moves):
    start_x = force_field[1].index(".")
    my_elephant = MyElephant(start_x, force_field)
    for move in moves:
        my_elephant.next_move(move)

    return my_elephant.get_password()


class MyElephant:
    col: int
    row: int = 1
    facing: int = 0  # 0 >  ;  1 v  ;  2 <  ;  3 ^

    def __init__(self, col, force_field):
        self.col = col
        self.ff = force_field

    def __repr__(self):
        return f"<{self.row},{self.col}: {self.facing}>"

    def get_password(self):
        """
        return 1000 * x + 4 * y + facing
        """
        # print(f"Values on finish: {self.col=}  {self.row=} {self.facing=}")
        return 1000 * self.row + 4 * self.col + self.facing

    def get_position_values(self) -> tuple[int, int]:
        """
        param step can be 1 or -1
        """
        col = self.col
        row = self.row

        if self.facing == 0:  # right >
            col = self.col + 1
        elif self.facing == 1:  # down v
            row = self.row + 1
        elif self.facing == 2:  # left <
            col = self.col - 1
        elif self.facing == 3:  # up ^
            row = self.row - 1
        else:
            raise ValueError(f"This facing is wrong '{self.facing}'")

        return row, col

    def next_move(self, move):
        if isinstance(move, str):
            if move == "L":
                if self.facing == 0:
                    self.facing = 3
                else:
                    self.facing -= 1
            elif move == "R":
                if self.facing == 3:
                    self.facing = 0
                else:
                    self.facing += 1
        elif isinstance(move, int):
            self.go_steps(move)

    def go_steps(self, steps_count):
        for i in range(1, steps_count + 1):
            tile_row, tile_col = self.get_position_values()

            if self.is_tile_stops(tile_row, tile_col):
                return

    def is_tile_stops(self, tile_row, tile_col, facing=None) -> bool:
        tile = self.ff[tile_row][tile_col]
        match tile:
            case "#":
                return True
            case ".":
                self.next_step(tile, tile_row, tile_col, facing)
            case " ":
                return self.jump_to_other_side(tile_row, tile_col)
            case tile:
                return self.jump_to_letter_side(tile)
        return False

    def next_step(self, tile, tile_row, tile_col, facing=None):
        self.col = tile_col
        self.row = tile_row

        if facing is not None:
            self.facing = facing

    def jump_to_other_side(self, tile_row, tile_col):
        if self.facing == 0:  # for right check on the max left
            tile = "."
            col = self.col
            while tile != " ":
                col -= 1
                tile = self.ff[self.row][col]
            return self.is_tile_stops(self.row, col + 1)

        elif self.facing == 1:  # for down check on the max up
            tile = "."
            row = self.row
            while tile != " ":
                row -= 1
                tile = self.ff[row][self.col]
            return self.is_tile_stops(row + 1, self.col)
        elif self.facing == 2:
            tile = "."
            col = self.col
            while tile != " ":
                col += 1
                tile = self.ff[self.row][col]
            return self.is_tile_stops(self.row, col - 1)
        elif self.facing == 3:
            tile = "."
            row = self.row
            while tile != " ":
                row += 1
                tile = self.ff[row][self.col]
            return self.is_tile_stops(row - 1, self.col)

    def jump_to_letter_side(self, tile):
        match tile:
            case "A":
                tile_col = 1
                tile_row = self.col + 100
                facing = 0
            case "B":
                tile_col = self.col - 100
                tile_row = 200
                facing = 3
            case "C":
                tile_col = 100
                tile_row = 151 - self.row
                facing = 2
            case "D":
                tile_col = 100
                tile_row = self.col - 50
                facing = 2
            case "E":  # done
                tile_col = self.row + 50
                tile_row = 50
                facing = 3
            case "F":  # done
                tile_col = 150
                tile_row = 151 - self.row
                facing = 2
            case "G":  # done
                tile_col = 50
                tile_row = 100 + self.col
                facing = 2
            case "H":  # done
                tile_col = self.row - 100
                tile_row = 150
                facing = 3
            case "I":  # done
                tile_col = self.col + 100
                tile_row = 1
                facing = 1
            case "J":  # done
                tile_col = self.row - 100
                tile_row = 1
                facing = 1
            case "K":  # done
                tile_col = 51
                tile_row = 151 - self.row
                facing = 0
            case "L":  # done
                tile_col = 51
                tile_row = 50 + self.col
                facing = 0
            case "M":  # done
                tile_col = self.row - 50
                tile_row = 101
                facing = 1
            case "N":
                tile_col = 1
                tile_row = 151 - self.row
                facing = 0
            case "X":
                if self.col == 100:
                    tile_col = 101
                    tile_row = 50
                    facing = 3
                else:
                    tile_col = 100
                    tile_row = 51
                    facing = 2
            case letter:
                # "Y" or "Z":
                print(f"ERROR: This letter is '{letter}' not ready")
                raise NotImplemented()
        self.debug(tile, tile_row, tile_col, facing)
        return self.is_tile_stops(tile_row, tile_col, facing)

    def debug(self, tile, tile_row, tile_col, facing):
        r1, c1 = self.get_position_values()
        tile_to_move = self.ff[r1][c1]
        if tile == tile_to_move:
            check_to_letter = L_RANGES[tile][4]

            if facing == 0:
                tile_col = tile_col - 1  # reverse for right >
            elif facing == 1:
                tile_row = tile_row - 1  # reverse for down v
            elif facing == 2:
                tile_col = tile_col + 1  # reverse for left <
            elif facing == 3:
                tile_row = tile_row + 1  # reverse for up ^

            dest_tile_letter = self.ff[tile_row][tile_col]
            if check_to_letter != dest_tile_letter:
                raise ValueError(f"{check_to_letter=}   !=  {dest_tile_letter=}")
        else:
            raise ValueError(f"NOT OK {tile} != {tile_to_move}")


force_field_data, moves_data = read_input()
password = simulate(force_field_data, moves_data)
print(f"The first password is {password}")

form_cube(force_field_data)
# show(force_field_data)

password2 = simulate(force_field_data, moves_data)
print(f"The second password is {password2}")
