#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 12"""

# stdlib imports
import dataclasses
from typing import List, Tuple

# 3rd party lib imports

# own stuff
import utils

InstrType = List[Tuple[str, int]]
S_EAST = "E"
S_WEST = "W"
S_NORTH = "N"
S_SOUTH = "S"
S_FORWARD = "F"
S_LEFT = "L"
S_RIGHT = "R"

TURNS_DICT = {
    S_EAST: [S_EAST, S_SOUTH, S_WEST, S_NORTH],
    S_SOUTH: [S_SOUTH, S_WEST, S_NORTH, S_EAST],
    S_WEST: [S_WEST, S_NORTH, S_EAST, S_SOUTH],
    S_NORTH: [S_NORTH, S_EAST, S_SOUTH, S_WEST],
}


@dataclasses.dataclass
class Point:
    x: int
    y: int

    def __add__(self, other: "Point"):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int):
        return Point(self.x * other, self.y * other)

    def __rmul__(self, other):
        # "Point() * 3" works with __mul__, but "3 * Point()" does not... that's
        # what "__rmul__" is for
        return self * other

    def manhattan_dist(self):
        """manhattan distance from the origin"""
        return manhattan_distance(self.x, self.y)

    def rotate(self, n_turns) -> "Point":
        """rotate clockwise (right) n_turns times 90 degrees"""
        x, y = self.x, self.y
        for _ in range(n_turns):
            x, y = y, -x

        return Point(x, y)


def parse_instructions(input_raw: str) -> InstrType:
    return [(elem[0], int(elem[1:])) for elem in input_raw.strip().split("\n")]


def run_instructions_ship(instructions: InstrType) -> Tuple[int, int]:
    """run the instructions and return the end position as (x, y) coordinate"""
    facing = S_EAST
    x, y = 0, 0
    for instr, num in instructions:

        if instr in [S_LEFT, S_RIGHT]:
            if instr == S_LEFT:
                num *= -1

            n_turns = (num % 360) // 90
            facing = TURNS_DICT[facing][n_turns]

        if instr == S_FORWARD:
            instr = facing

        if instr == S_NORTH:
            y += num

        if instr == S_SOUTH:
            y -= num

        if instr == S_WEST:
            x -= num

        if instr == S_EAST:
            x += num

    return x, y


def run_instructions_waypoint(instructions: InstrType) -> Point:
    """run the instructions and return the end position as (x, y) coordinate"""
    waypoint = Point(10, 1)
    pos = Point(0, 0)

    for instr, num in instructions:

        if instr in [S_LEFT, S_RIGHT]:
            if instr == S_LEFT:
                num = 360 - (num % 360)
            n_turns = num % 360 // 90
            waypoint = waypoint.rotate(n_turns)

        if instr == S_NORTH:
            waypoint.y += num

        if instr == S_SOUTH:
            waypoint.y -= num

        if instr == S_WEST:
            waypoint.x -= num

        if instr == S_EAST:
            waypoint.x += num

        # ship moves towards waypoint
        if instr == S_FORWARD:
            pos += num * waypoint

    return pos


def manhattan_distance(x: int, y: int) -> int:
    """compute the manhattan distance"""
    return abs(x) + abs(y)


def main() -> None:
    instructions = parse_instructions(utils.get_input(__file__))

    # part 1
    dist_part_1 = manhattan_distance(*run_instructions_ship(instructions))
    print(f"part 1: {dist_part_1}")

    # part 2
    dist_part_2 = run_instructions_waypoint(instructions).manhattan_dist()
    print(f"part 2: {dist_part_2}")


if __name__ == "__main__":
    main()
