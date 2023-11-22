#!/usr/bin/env python3
"""
https://adventofcode.com/2021/day/16
"""
import math
from typing import Self

FILENAME = "day16.input.txt"
TYPE_ID_LITERAL = 4


class Transmission:
    cache = ""
    versions_sum = 0

    def __init__(self, data: str):
        self.data = [l for l in data]

    def __repr__(self):
        return f"<{''.join(self.data[:20])}>"

    def get_bits(self, count: int) -> str:
        while len(self.cache) < count:
            self.cache = f"{self.cache}{int(self.data.pop(0), base=16):04b}"

        bits, self.cache = self.cache[:count], self.cache[count:]
        return bits

    def is_data(self) -> bool:
        return bool(self.data) or bool(self.cache)

    def drop_0(self):
        if "1" not in self.cache:
            self.cache = ""

        while self.data and self.data[0] == "0":
            self.data.pop(0)

    def process_packages(self, parent=None):
        package = Package(self, parent)
        package.read_data()

        if parent:
            parent.childs.append(package)
            parent.subtract_length(package.length)
        else:
            self.drop_0()

        return package


class Package:
    version: int
    type_id: int
    value: int
    transmission: Transmission
    parent: [Self] = None
    subpackages_length: int = 0
    subpackages_count: int = 0
    length: int = 0
    version: int
    type_id: int
    bits: str = ""
    data: int
    is_literal: bool = False

    def __init__(self, transmission, parent):
        self.transmission = transmission
        self.parent = parent
        self.childs = []
        self.set_header()
        if self.type_id == TYPE_ID_LITERAL:
            self.is_literal = True

    def __repr__(self):
        return f"<P{'l' if self.is_literal else 'o'} {self.version}, {self.bits}>"

    def get_bits(self, count: int):
        self.add_length(count)
        return self.transmission.get_bits(count)

    def add_length(self, length: int):
        self.length += length
        if self.parent:
            self.parent.add_length(length)

    def set_header(self):
        self.version = int(self.get_bits(3), base=2)
        self.transmission.versions_sum += self.version
        self.type_id = int(self.get_bits(3), base=2)

    def get_packets_data(self) -> [str]:
        while True:
            bits = self.get_bits(5)
            yield bits[1:]
            if bits[0] == "0":
                return

    def read_data(self):
        if self.is_literal:
            for bits in self.get_packets_data():
                self.bits = f"{self.bits}{bits}"
            self.value = int(self.bits, base=2)
            # print(f"literal: {self.value}, \t {self.bits}")
        else:
            self.get_operator()

    def get_operator(self):
        self.get_length_type_id()
        while self.is_packages_reading():
            self.transmission.process_packages(self)

    def get_length_type_id(self):
        length_type_id = self.get_bits(1)
        if length_type_id == "0":
            self.subpackages_length = int(self.get_bits(15), base=2)
        else:
            self.subpackages_count = int(self.get_bits(11), base=2)

    def subtract_length(self, length):
        if self.subpackages_length:
            self.subpackages_length -= length
        if self.subpackages_count:
            self.subpackages_count -= 1

    def is_packages_reading(self) -> bool:
        return bool(self.subpackages_count) or bool(self.subpackages_length)

    def get_result(self):
        match self.type_id:
            case 0:
                return sum(p.get_result() for p in self.childs)
            case 1:
                return math.prod(p.get_result() for p in self.childs)
            case 2:
                return min(p.get_result() for p in self.childs)
            case 3:
                return max(p.get_result() for p in self.childs)
            case 4:
                return self.value
            case 5:
                return 1 if self.childs[1].get_result() < self.childs[0].get_result() else 0
            case 6:
                return 1 if self.childs[0].get_result() < self.childs[1].get_result() else 0
            case 7:
                return 1 if self.childs[0].get_result() == self.childs[1].get_result() else 0


def read_input(filename):
    with open(filename, "r") as f:
        return f.read()


def decode_t2(data):
    tr = Transmission(data)
    package = None
    while tr.is_data():
        package = tr.process_packages()

    return package, tr.versions_sum


if __name__ == "__main__":
    data = read_input(FILENAME)
    package, version_sum = decode_t2(data)
    print(f"Versions sum is {version_sum}")
    res = package.get_result()
    print(f"Packages calculated expression is {res}")
