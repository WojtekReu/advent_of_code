#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/10
"""
MATCHING_CHUNKS = ("()", "[]", "{}", "<>")
CHUNK_POINTS = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}


def read_input(filename):
    with open(filename, "r") as f:
        data = f.read()
    return data


def calculate_scores(ns_data):
    sum_scores = 0
    cs_score_list = []
    for row in ns_data.split("\n"):
        stock = []
        correct_chunk = True
        for chunk in row:
            if chunk in "[({<":
                stock.append(chunk)
            else:
                last_chunk = stock.pop()
                check_chunk = f"{last_chunk}{chunk}"
                if check_chunk not in MATCHING_CHUNKS:
                    if chunk == ")":
                        sum_scores += 3
                    elif chunk == "]":
                        sum_scores += 57
                    elif chunk == "}":
                        sum_scores += 1197
                    elif chunk == ">":
                        sum_scores += 25137
                    correct_chunk = False

        if correct_chunk:
            cs_score = 0
            while stock:
                chunk = stock.pop()
                points = CHUNK_POINTS[chunk]
                cs_score = cs_score * 5 + points
            cs_score_list.append(cs_score)

    m_scores_index = int(len(cs_score_list) / 2)
    m_score = sorted(cs_score_list)[m_scores_index]

    return sum_scores, m_score


if __name__ == "__main__":
    data = read_input("day10.input.txt")
    tse_score, m_score = calculate_scores(data)
    print(f"Total syntax error score is {tse_score} and middle score is {m_score}.")
