#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/19
"""
from math import prod


def read_input() -> list:
    with open("day19.input.txt", "r") as f:
    # with open('day19.test.txt', "r") as f:
        data = f.read()

    blueprints = []
    for line in data.split("\n"):
        blueprint_words = line.split(":")
        blueprint_nr = blueprint_words[0][-2:].strip()
        blueprint = Blueprint(blueprint_nr)
        blueprints.append(blueprint)
        for bp_line in blueprint_words[1].split("."):
            if not bp_line:
                continue
            words = bp_line.strip().split()
            costs_clay = costs_obsidian = 0
            costs_ore = words[4]
            if words[-1] == "clay":
                costs_clay = words[7]
            elif words[-1] == "obsidian":
                costs_obsidian = words[7]
            robot_type = blueprint.create_robot_type(words[1])
            robot_type.add_cost(costs_ore, costs_clay, costs_obsidian)

    return blueprints


def show(blueprints):
    for blueprint in blueprints:
        print(blueprint)
        for name, robot_type in blueprint.robot_types.items():
            print(name, robot_type, robot_type.costs)


def simulate(blueprints, minutes, is_p2=False):
    quality_level = {}
    for nr, blueprint in enumerate(blueprints, start=1):
        resources = blueprint.run_plan(minutes)
        quality_level[nr] = resources[7]
        # print(f"ID: {nr} resources: {resources}")

    if is_p2:
        return prod(quality_level.values())
    else:
        return sum(tuple(k * v for k, v in quality_level.items()))


def add_wallet(new_wallets, robots, new_robots, new_resources):
    new_resources = tuple(sum(c) for c in zip(robots, new_resources))
    wallet = new_robots + new_resources
    new_wallets.add(wallet)


class RobotType:
    name: str
    costs: tuple = None

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<RT {self.name}>"

    def add_cost(self, costs_ore, costs_clay, costs_obsidian):
        self.costs = int(costs_ore), int(costs_clay), int(costs_obsidian), 0

    def consume(self, wallet):
        return (
            wallet[0] - self.costs[0],
            wallet[1] - self.costs[1],
            wallet[2] - self.costs[2],
            wallet[3],
        )

    def can_build(self, wallet):
        if (
            self.costs[0] <= wallet[0]
            and self.costs[1] <= wallet[1]
            and self.costs[2] <= wallet[2]
        ):
            return True
        return False


class Blueprint:
    def __init__(self, nr):
        self.nr = int(nr)
        self.robot_types: dict[str, RobotType] = {}

    def __repr__(self):
        return f"<{self.nr}>"

    def create_robot_type(self, name: str):
        robot_type = RobotType(name)
        self.robot_types[name] = robot_type
        return robot_type

    def run_plan(self, minutes):
        geode = self.robot_types["geode"]
        obsidian = self.robot_types["obsidian"]
        clay = self.robot_types["clay"]
        ore = self.robot_types["ore"]
        wallets = set()
        wallets.add((1, 0, 0, 0, 0, 0, 0, 0))
        for minute in range(1, minutes + 1):
            # print(f"minute = {minute}")
            new_wallets = set()

            for wallet in wallets:
                robots = wallet[:4]
                resources = wallet[4:]
                if geode.can_build(resources):
                    new_resources = geode.consume(resources)
                    new_robots = (robots[0], robots[1], robots[2], robots[3] + 1)
                    add_wallet(new_wallets, robots, new_robots, new_resources)

                if obsidian.can_build(resources):
                    new_resources = obsidian.consume(resources)
                    new_robots = (robots[0], robots[1], robots[2] + 1, robots[3])
                    add_wallet(new_wallets, robots, new_robots, new_resources)

                if clay.can_build(resources):
                    new_resources = clay.consume(resources)
                    new_robots = (robots[0], robots[1] + 1, robots[2], robots[3])
                    add_wallet(new_wallets, robots, new_robots, new_resources)

                if ore.can_build(resources):
                    new_resources = ore.consume(resources)
                    new_robots = (robots[0] + 1, robots[1], robots[2], robots[3])
                    add_wallet(new_wallets, robots, new_robots, new_resources)

                new_wallets.add(robots + tuple(sum(c) for c in zip(robots, resources)))

            wallets = set()
            for i in range(8):
                max_type = max(new_wallets, key=lambda x: x[i])[i]

                if max_type > 0:
                    for wallet in new_wallets:
                        if wallet[i] > max_type - 2:
                            wallets.add(wallet)

        return max(wallets, key=lambda w: w[7])


MINUTES = 24
MINUTES_P2 = 32

blueprints_data = read_input()
show(blueprints_data)

result = simulate(blueprints_data, MINUTES)
print(f"Sum of the quality level for all blueprints is {result} for {MINUTES} minutes.")

result2 = simulate(blueprints_data[:3], MINUTES_P2, True)
print(
    f"When you multiply the first 3 blueprints you have {result2} for {MINUTES_P2} minutes."
)
