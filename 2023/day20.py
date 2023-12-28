#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/20
real time  0m0,384s
"""
from collections import deque
from copy import deepcopy
from math import lcm

FILENAME_TEST1 = "day20.test.1.txt"
FILENAME_TEST2 = "day20.test.2.txt"
FILENAME_INPUT = "day20.input.txt"


class Module:
    prefix: str
    repr: str
    count_low: int = 0
    count_high: int = 0
    pulse: [int] = None

    def __init__(self, name: str):
        self.name = name
        self.destinations = []
        self._create_repr()

    def __repr__(self):
        return self.repr

    def _create_repr(self):
        if not self.destinations:
            self.repr = f"{self.prefix}{self.name}"
        elif isinstance(self.destinations[0], str):
            self.repr = (
                f"{self.prefix}{self.name} -> {', '.join(name for name in self.destinations)}"
            )
        else:
            self.repr = (
                f"{self.prefix}{self.name} -> {', '.join(d.name for d in self.destinations)}"
            )

    def add_destination(self, module_name):
        self.destinations.append(module_name)
        self._create_repr()

    def send(self):
        for destination in self.destinations:
            # print(f"{self.name} -{'high' if self.pulse else 'low'}-> {destination.name}")
            destination.set_pulse(self.name, self.pulse)
            yield self.name, self.pulse, destination

    def set_pulse(self, _, pulse):
        self.pulse = pulse

    def increase_count(self):
        for i in range(len(self.destinations)):
            if self.pulse == 1:
                self.count_high += 1
            else:
                self.count_low += 1


class FlipFlop(Module):
    prefix = "%"
    state = False  # off

    def process(self, name, pulse) -> [int]:
        if pulse == 0:  # low pulse
            self.switch_state()
            self.pulse = 1 if self.state else 0  # 0 if "on(True)" else 1
            self.increase_count()
            return True

    def switch_state(self) -> None:
        self.state = not self.state


class Conjunction(Module):
    prefix = "&"

    def __init__(self, *args):
        self.pulses = {}
        super().__init__(*args)

    def add_input(self, module):
        self.pulses[module.name] = 0

    def process(self, name, pulse) -> [int]:
        self.set_pulse(name, pulse)
        self.pulse = 0 if all(self.pulses.values()) else 1
        self.increase_count()
        return True

    def set_pulse(self, name, pulse):
        self.pulses[name] = pulse


class Broadcaster(Module):
    prefix = ""

    def process(self, *args):
        self.increase_count()
        return True


class Output(Module):
    prefix = ""

    def process(self, *args):
        pass


def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def prepare(data: str):
    modules = {"button": Broadcaster("button")}
    modules["button"].destination_names = ["broadcaster"]
    for line in data.split("\n"):
        words = line.split()
        prefix = words[0][0]
        if prefix == "%":
            module = FlipFlop(words[0][1:])
        elif prefix == "&":
            module = Conjunction(words[0][1:])
        else:
            module = Broadcaster(words[0])

        module.destination_names = [d.strip(",") for d in words[2:]]
        modules[module.name] = module

    for module in modules.values():
        for d_name in module.destination_names:
            try:
                destination = modules[d_name]
            except KeyError:
                destination = Output(d_name)
            module.add_destination(destination)
            if isinstance(destination, Conjunction):
                destination.add_input(module)

    return modules


def press_button(modules):
    module_start = modules["button"]
    module_start.set_pulse("", 0)
    modules_process = deque()
    modules_process.append(("", 0, module_start))

    while modules_process:
        src, pulse, module = modules_process.popleft()
        res = module.process(src, pulse)
        if res:
            for m2 in module.send():
                modules_process.append(m2)


def calculate(modules: dict[str, FlipFlop | Conjunction | Broadcaster]):
    for i in range(1000):
        press_button(modules)

    count_low = count_high = 0
    for name, m in modules.items():
        count_low += m.count_low
        count_high += m.count_high

    return count_low * count_high


def check_pulses(modules, gq_sources_press_button_counts, press_button_count):
    is_visited = False
    for name, pulse in gq_sources_press_button_counts.items():
        if pulse == 0 and modules[name].count_high != 0:
            gq_sources_press_button_counts[name] = press_button_count
            is_visited = True
    return is_visited


def calculate2(modules: dict[str, FlipFlop | Conjunction | Broadcaster]):
    gq = modules["gq"]  # &gq -> rx
    press_button_count = 0
    gq_sources_press_button_counts = deepcopy(gq.pulses)
    while gq.count_low == 0:
        press_button(modules)
        press_button_count += 1
        if check_pulses(modules, gq_sources_press_button_counts, press_button_count):
            if all(gq_sources_press_button_counts.values()):
                return lcm(*list(gq_sources_press_button_counts.values()))

    return press_button_count


if __name__ == "__main__":
    data = read_input(FILENAME_INPUT)
    m = prepare(data)
    res1 = calculate(m)
    print(f"If you multiply the total number of low and high pulses you get {res1}.")
    assert res1 == 832957356

    m = prepare(data)
    res2 = calculate2(m)
    print(
        f"The fewest number of button presses required to deliver a single low pulse to the module rx is {res2}."
    )
    assert res2 == 240162699605221
