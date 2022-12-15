#!/usr/bin/env python3
"""
https://adventofcode.com/2022/day/15
"""

COORD_Y = 2_000_000
# COORD_Y = 10
MULTIPLIER = 4_000_000
SEARCH_RANGE_MIN = 0
SEARCH_RANGE_MAX = 4_000_000
# SEARCH_RANGE_MAX = 20


def read_input() -> list:
    with open('day15_input.txt', "r") as f:
    # with open('test.txt', "r") as f:
        data = f.read()

    sensors = []
    for nr, line in enumerate(data.split("\n")):
        # print(line)
        words = line.split()
        x_str = words[-2].rstrip(',').lstrip('x=')
        y_str = words[-1].lstrip('y=')
        beacon = Beacon(int(x_str), int(y_str), nr)

        x_str = words[2].rstrip(',').lstrip('x=')
        y_str = words[3].rstrip(':').lstrip('y=')
        sensor = Sensor(int(x_str), int(y_str), nr, beacon)
        sensors.append(sensor)

    return sensors


def add_range(ranges, c):
    if not ranges:
        ranges.append(c)
        return

    new_range = None
    reversed_index_join = []
    append_range = True
    insert_index = None

    for i, r in enumerate(ranges):
        if r[0] <= c[0] <= r[1]:
            if r[1] < c[1]:
                new_range = r[0], c[1]
                reversed_index_join.insert(0, i)
            else:
                append_range = False
                break

        elif r[0] <= c[1] <= r[1]:
            if c[0] < r[0]:
                if new_range:
                    new_range = new_range[0], r[1]
                else:
                    new_range = c[0], r[1]
                reversed_index_join.insert(0, i)
                break

        elif c[0] <= r[0] and r[1] <= c[1]:
            if new_range:
                new_range = new_range[0], c[1]
            else:
                new_range = c[0], c[1]
            reversed_index_join.insert(0, i)

        if c[1] < r[0]:
            insert_index = i
            break

    if new_range:
        index = reversed_index_join.pop()
        ranges[index] = new_range
        if reversed_index_join:
            for index in reversed_index_join:
                del ranges[index]
    elif insert_index is not None:
        ranges.insert(insert_index, c)
    elif append_range:
        ranges.append(c)


def find_positions(sensors, coord_y):
    coords_x_for_y = []
    for sensor in sensors:
        sensor_range = abs(sensor.x - sensor.beacon.x) + abs(sensor.y - sensor.beacon.y)
        if sensor.y - sensor_range <= coord_y <= sensor.y + sensor_range:
            dy = abs(sensor.y - coord_y)
            dx = sensor_range - dy
            if dx:
                add_range(coords_x_for_y, (sensor.x - dx, sensor.x + dx))
            else:
                add_range(coords_x_for_y, (sensor.x, sensor.x))

            # print(sensor, sensor.beacon, sensor_range, dx)

    for sensor in sensors:
        if sensor.beacon.y == coord_y:
            try:
                index = coords_x_for_y.index(sensor.beacon.x)
                del coords_x_for_y[index]
            except ValueError:
                pass

    return coords_x_for_y


def find_beacon(sensors):
    for check_y in range(SEARCH_RANGE_MAX+1):
        r_list = find_positions(sensors, check_y)
        scope = SEARCH_RANGE_MIN, SEARCH_RANGE_MAX
        hash = scope
        for pair in ranges_list:
            if hash[0] <= pair[1] <= hash[1]:
                if pair[0] <= hash[0]:
                    hash = pair[1], hash[1]
                else:
                    raise ValueError(f'Divided_1: {check_y=}, {pair=}  --  {hash}')
            elif hash[0] <= pair[0] <= hash[1]:
                if hash[1] <= pair[1]:
                    hash = hash[0], pair[0]
                else:
                    raise ValueError(f'Divided_2: {check_y=}, {pair=}  --  {hash}')

        if hash != scope:
            if 1 < hash[1] - hash[0]:
                check_x = hash[0] + 1
                return check_x, check_y


class Beacon:

    def __init__(self, x, y, nr):
        self.x = x
        self.y = y
        self.nr = nr

    def __repr__(self):
        return f"<B ({self.x},{self.y})>"


class Sensor:
    beacon: Beacon

    def __init__(self, x, y, nr, beacon):
        self.x = x
        self.y = y
        self.nr = nr
        self.beacon = beacon

    def __repr__(self):
        return f"<S{self.nr} ({self.x},{self.y})>"


sensors_data = read_input()
# for s in sensors_data:
#     print(s)
ranges_list = find_positions(sensors_data, COORD_Y)

range_sum = 0
for pair in ranges_list:
    range_sum = range_sum + (pair[1] - pair[0])

print(f"Beacon can not contain {range_sum} positions.")

beacon_position = find_beacon(sensors_data)

tuning_frequency = beacon_position[0] * MULTIPLIER + beacon_position[1]
print(f"For position {beacon_position} found tuning frequency {tuning_frequency}.")
