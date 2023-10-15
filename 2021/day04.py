#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/4
"""
with open("day04.input.txt", "r") as f:
    data = f.read().split("\n")


def prepare_draw_numbers(data) -> list[str]:
    return [v for v in data[0].split(",")]


def prepare_boards(data) -> list[list[list[str]]]:
    boards = []
    table = []
    for row in data[1:]:
        if not row:
            if table:
                cols = []
                for i in range(len(table[0])):
                    cols.append([row[i] for row in table])
                # table has list with rows and cols.
                table += cols
                boards.append(table)
            table = []
        else:
            table.append([v for v in row.split()])
    return boards


def calculate_score(turn, board):
    # board has duplicated values 5 lists as rows and 5 lists as board columns
    # to calculate sum you can use only rows or only columns
    board_sum = sum([int(el) for row in board[:5] for el in row if isinstance(el, str)])
    return int(turn) * board_sum


def board_move(turn, board):
    for row in board:
        for i, el in enumerate(row):
            if el == turn:
                row[i] = int(row[i])
        for el in row:
            if isinstance(el, str):
                break
        else:
            scores = calculate_score(turn, board)
            return turn, scores


def start_game(boards: list, draw_numbers: list, is_first: bool):
    turn_for_scores = 0
    scores = 0

    for turn in draw_numbers:
        remove_boards = []
        for board in boards:
            scores = board_move(turn, board)
            if scores:
                if is_first:
                    return turn, scores
                else:
                    turn_for_scores = turn
                    remove_boards.append(board)

        for b in remove_boards:
            boards.remove(b)

    return turn_for_scores, scores


draw_numbers = prepare_draw_numbers(data)
boards = prepare_boards(data)
turn, scores = start_game(boards, draw_numbers, True)
print(f"First board wins in turn {turn}, score is {scores}.")

turn, scores = start_game(boards, draw_numbers, False)
print(f"Last board wins in turn {turn}, score is {scores}.")
