#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/04
real time	0m3,131s
"""
FILENAME = "day04.input.txt"


def read_input(filename):
    with open(filename, "r") as f:
        return f.read()


def prepare(data):
    cards = []
    for line in data.split("\n"):
        parts = line.split(":")[1].split("|")
        winning = set(int(v) for v in parts[0].split())
        you_have = set(int(v) for v in parts[1].split())
        cards.append((winning, you_have))
    return cards


def calculate(cards):
    your_points = 0
    for card in cards:
        card_points = 0
        for v in card[1]:
            if v in card[0]:
                if not card_points:
                    # first card has 1 point
                    card_points = 1
                else:
                    # every next card double your card points
                    card_points *= 2
        your_points += card_points
    return your_points


def calculate2(cards):
    cards_copy = {}
    for c_id, card in enumerate(cards, 1):
        card_count = 0
        for v in card[1]:
            if v in card[0]:
                card_count += 1
        cards_copy[c_id] = [c_id + n for n in range(1, card_count + 1)]

    res = count_cards(cards_copy)
    return res


def count_cards(cards):
    sum_cards = 0

    for c_id, card_list in cards.items():
        sum_cards += 1
        for n_card in card_list:
            sum_cards += count_children(n_card, cards)
    return sum_cards


def count_children(c_id, cards):
    sum_cards = 1
    for n_card in cards[c_id]:
        sum_cards += count_children(n_card, cards)

    return sum_cards


if __name__ == "__main__":
    data = read_input(FILENAME)
    c = prepare(data)
    result = calculate(c)
    print(f"Scratchcards are worth {result} in total.")
    result2 = calculate2(c)
    print(f"You end up with {result2} scratchcards.")
