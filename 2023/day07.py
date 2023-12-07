#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/07
real time  0m0,044s
"""
FILENAME = "day07.input.txt"


class Hand:
    value: int = 0
    joker_replacement: str = ""
    LABELS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    L_JOKE = ["0", "J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]

    def __init__(self, labels, bid, with_jokers):
        self.labels: str = labels
        self.labels2: str = labels
        self.bid: int = int(bid)
        self.with_jokers = with_jokers
        if self.with_jokers:
            self.replace_jokers()
        self.calculate_values()

    def __repr__(self):
        if self.joker_replacement:
            return f"<{self.labels} {self.bid}  (J:{self.joker_replacement })>"
        return f"<{self.labels} {self.bid}>"

    def get_pattern_order(self):
        return self.L_JOKE if self.with_jokers else self.LABELS

    def jocker_to(self, c):
        self.joker_replacement = c
        self.labels2 = self.labels.replace("J", c)

    def jocker_to_highest(self):
        hl = self.find_highest_label()
        self.jocker_to(hl)

    def find_highest_label(self):
        return max(self.labels, key=lambda x: self.get_pattern_order().index(x))

    def replace_jokers(self):
        if self.labels == "JJJJJ":
            self.jocker_to("A")
        elif self.labels.count("J") == 4:
            for c in self.labels:
                if c != "J":
                    self.jocker_to(c)
                    break

        elif self.labels.count("J") == 3:
            self.jocker_to_highest()

        elif self.labels.count("J") == 2:
            for c in self.labels:
                if self.labels.count(c) == 2 and c != "J":
                    self.jocker_to(c)
                    break
            else:
                self.jocker_to_highest()

        elif self.labels.count("J") == 1:
            for c in self.labels:
                if self.labels.count(c) == 3 and c != "J":
                    self.jocker_to(c)
                    break
            else:
                for c in self.labels:
                    if self.labels.count(c) == 2 and c != "J":
                        self.jocker_to(c)
                        break
                else:
                    self.jocker_to_highest()
        else:
            self.labels2 = self.labels

    def calculate_values(self):
        for c in self.labels2:
            if self.labels2.count(c) == 5:
                self.value += 10_000_000_000
            if self.labels2.count(c) == 4:
                self.value += 8_000_000_000
            if self.labels2.count(c) == 3:
                self.value += 2_000_000_000
            if self.labels2.count(c) == 2:
                self.value += 1_000_000_000

        value_str = ""
        for i, c in enumerate(self.labels):
            value = self.get_pattern_order().index(c)
            value_str = f"{value_str}{value:02}"

        self.value += int(value_str)


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str, with_jokers: bool = False):
    hands = []
    for line in data.split("\n"):
        words = line.split()
        hand = Hand(words[0], words[1], with_jokers)
        hands.append(hand)
    return hands


def calculate(hands):
    hands.sort(key=lambda x: x.value)
    values_bids_sum = 0

    for i, hand in enumerate(hands, 1):
        # print(hand)
        values_bids_sum += hand.bid * i

    return values_bids_sum


if __name__ == "__main__":
    data = read_input(FILENAME)
    r = prepare(data)
    result = calculate(r)
    print(f"The total winnings are: {result}.")
    assert result == 246409899

    r2 = prepare(data, True)
    result2 = calculate(r2)
    print(f"The total winnings with jokers replacement are: {result2}")
    assert result2 == 244848487
