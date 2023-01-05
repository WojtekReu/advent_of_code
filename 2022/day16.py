#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/16
"""

from collections import deque


def read_input() -> dict:
    with open("day16.input.txt", "r") as f:
    # with open('day16.test.txt', "r") as f:
        data = f.read()

    valves: [str, Valve] = {}
    tunnels = {}
    for nr, line in enumerate(data.split("\n")):
        # print(line)
        words = line.split()
        name = words[1]
        rate = words[4].split("=")[1].rstrip(";")
        valve = Valve(name, rate)
        valves[name] = valve
        tunnels[name] = [name.rstrip(",") for name in words[9:]]
    for valve_begin_name, valve_end_names in tunnels.items():
        valve_begin = valves[valve_begin_name]
        for valve_end_name in valve_end_names:
            valve_end = valves[valve_end_name]
            valve_begin.valves[
                valve_end
            ] = 2  # 1 minute to step + 1 minute for open valve

    return valves


def join_valves(valves: dict):
    for name, valve in valves.items():
        valve_queue = deque()
        valve.valves_tmp = {}
        for valve_next, time_steps in valve.valves.items():
            valve_next.time_steps = time_steps
            valve_queue.appendleft(valve_next)
            valve.valves_tmp[valve_next] = time_steps

        while valve_queue:
            valve_end = valve_queue.popleft()
            if valve_end is not valve and valve_end not in valve.valves_tmp.keys():
                valve.valves_tmp[valve_end] = valve_end.time_steps

            for valve_next, time_steps in valve_end.valves.items():
                if (
                    valve_next is not valve
                    and valve_next not in valve_queue
                    and valve_next not in valve.valves_tmp.keys()
                ):
                    valve_next.time_steps = valve_end.time_steps + 1
                    valve_queue.append(valve_next)


def remove_empty_rate_valves(valves: dict):
    for valve in valves.values():
        valve.valves = {}
        for valve_end, time_steps in valve.valves_tmp.items():
            if valve_end.rate:
                valve.valves[valve_end] = time_steps

        valve.__delattr__("valves_tmp")


class Valve:
    valves: dict

    def __init__(self, name, rate):
        self.name = name
        self.rate = int(rate)
        self.valves = {}

    def __repr__(self):
        return f"<{self.name},{self.rate}>"

    def open(self, traveler, time_left):
        traveler.opened_valves[self] = time_left * self.rate


class Traveler:
    valve: Valve = None
    max_released_pressure: int = 0

    def __init__(self, name, max_time, min_time_for_elephant=0):
        self.name: str = name
        self.opened_valves = {}
        self.max_time = max_time
        self.min_time_for_elephant = min_time_for_elephant

    def __repr__(self):
        if self.valve:
            return f"{self.name} = {self.valve}"
        return self.name

    def jump(self, minute):
        for valve, time_steps in self.valve.valves.items():
            if valve not in self.opened_valves.keys():
                time_left = self.max_time - minute - time_steps
                if time_left < self.min_time_for_elephant:
                    return self.call_after_time_left()
                valve.open(self, time_left)
                self.valve = valve
                self.jump(minute + time_steps)
                if valve in self.opened_valves.keys():
                    del self.opened_valves[valve]
        self.call_after_time_left()
        return self.max_released_pressure

    def call_after_time_left(self):
        if self.name == "p2":
            elephant = Traveler("elephant", self.max_time)
            elephant.valve = valve0
            elephant.opened_valves = self.opened_valves
            self.max_released_pressure = max(
                self.max_released_pressure, elephant.jump(0)
            )
        else:
            new_mrl = sum([pressure for pressure in self.opened_valves.values()])
            if self.max_released_pressure < new_mrl:
                self.max_released_pressure = new_mrl
                # print(f"Max released pressure for : {new_mrl}  ->   {self.opened_valves=} ")


def simulate(valve, traveler_name, max_time, min_time_for_elephant=0):
    traveler = Traveler(traveler_name, max_time, min_time_for_elephant)
    traveler.valve = valve
    return traveler.jump(0)


valves_data = read_input()
join_valves(valves_data)
remove_empty_rate_valves(valves_data)

valve0: Valve = valves_data["AA"]
MAX_TIME_P1 = 30
MAX_TIME_P2 = 26
MIN_TIME_FOR_ELEPHANT = 3  # 2 or 3 minutes traveler `left` for his elephant

max_released_pressure = simulate(valve0, "p1", MAX_TIME_P1)
print(f"Max released pressure for 1 traveler = {max_released_pressure}")

max_released_pressure2 = simulate(valve0, "p2", MAX_TIME_P2, MIN_TIME_FOR_ELEPHANT)
print(f"Max released pressure for traveler and his elephant = {max_released_pressure2}")
