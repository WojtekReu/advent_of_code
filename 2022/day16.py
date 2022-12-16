#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/16
"""


def read_input() -> list:
    with open('day16_input.txt', "r") as f:
    # with open('test.txt', "r") as f:
        data = f.read()

    valves = []
    valve_names = {}
    for nr, line in enumerate(data.split("\n")):
        print(line)
        words = line.split()
        name = words[1]
        rate = words[4].split('=')[1].rstrip(';')
        valve = Valve(name, rate)
        valves.append(valve)
        valve_names[name] = [name.rstrip(',') for name in words[9:]]
    # for name, valve_names_related in valve_names.items():
    for valve in valves:
        for name in valve_names[valve.name]:
            for valve1 in valves:
                if valve1.name == name:
                    valve.append(valve1)

    return valves


class Valve:
    priors: dict
    valves: list
    turn_count = 0

    def __init__(self, name, rate):
        self.name = name
        self.rate = int(rate)
        self.valves = []
        self.visited = []
        self.is_opened = False
        self.priors = {}

    def __repr__(self):
        return f"<{self.name},{self.rate}>"

    def append(self, valve):
        self.valves.append(valve)
        self.valves.sort(key=lambda v: v.rate, reverse=True)

    def open(self, time_left):
        self.is_opened = True
        return self.get_released_pressure(time_left)

    def cal_after_time_left(self, opened_valves, rlp):
        sum_rlp = sum(rlp)
        last_pressure.append(sum_rlp)
        print(f"PPP: {sum_rlp}  ->   {opened_valves=} ")
        rlp.pop()
        opened_valves.pop()
        return

    def get_released_pressure(self, time_left):
        return time_left * self.rate

    def set_on_the_end(self, valve):
        self.valves.remove(valve)
        self.valves.append(valve)

    def create_prior_table(self):
        self.step_jump = 0
        v_queue = [self]
        while v_queue:
            current_valve = v_queue.pop()
            for v in current_valve.valves:
                if v not in v_queue and v not in self.priors.keys():
                    v.step_jump = current_valve.step_jump + 1
                    v_queue.insert(0, v)

            if current_valve is not self:
                self.priors[current_valve] = (current_valve.step_jump + 1, current_valve.rate)
        to_remove = []
        for v, params in self.priors.items():
            if not params[1]:
                to_remove.append(v)
        for v in to_remove:
            del self.priors[v]

    def jump(self, minute, released_pressure, released_pressure_values, opened_valves):
        released_pressure_values.append(released_pressure)
        opened_valves.append(self)
        for valve, params in self.priors.items():
            if valve not in opened_valves:
                time_left = MAX_TIME - minute - params[0]
                if time_left < 0:
                    return valve.cal_after_time_left(opened_valves, released_pressure_values)
                released_pressure = valve.open(time_left)
                valve.jump(minute + params[0], released_pressure, released_pressure_values, opened_valves)

        return self.cal_after_time_left(opened_valves, released_pressure_values)


valves_data = read_input()
valve0 = None
for v in valves_data:
    if v.name == 'AA':
        valve0 = v
    v.create_prior_table()
    print(v, v.valves, v.priors)

MAX_TIME = 30
last_pressure = []

valve0.jump(0, 0, [], [])

for p in sorted(set(last_pressure)):
    print(f"pressure sum {p=}")

