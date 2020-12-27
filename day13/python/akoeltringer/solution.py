#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: add chinese remainder theorem


"""Solution of Problem of Day 13"""

# stdlib imports
import math
from typing import List, Tuple

# 3rd party lib imports

# own stuff
import utils


def parse_instructions(input_raw: str) -> Tuple[int, List[Tuple[int, int]]]:
    tta_str, bus_lines_raw = input_raw.strip().split("\n")
    bus_lines = [
        (i, int(e)) for i, e in enumerate(bus_lines_raw.split(",")) if e != "x"
    ]

    return int(tta_str), bus_lines


def compute_wait_time(tta: int, line: int) -> int:
    return (line - (tta % line)) % line


def find_line_next_depart(tta: int, bus_lines: List[Tuple[int, int]]) -> int:
    """find line which departs shortest after tta.
    Return waiting time * bus id
    """
    wait_table = {}

    for _, line in bus_lines:
        wait_time = compute_wait_time(tta, line)
        wait_table[wait_time] = line

    min_wait_time = min(wait_table.keys())
    return min_wait_time * wait_table[min_wait_time]


def find_earliest_tmsp_for_pattern_bf(bus_lines: List[Tuple[int, int]]) -> int:
    """compute brute force... lame!"""
    idx_max_line, max_line_num = max(bus_lines, key=lambda x: x[1])
    max_tmsp = 0

    while True:
        max_tmsp += max_line_num
        tmsp = max_tmsp - idx_max_line

        is_valid_list = [(tmsp + idx) % line == 0 for idx, line in bus_lines]
        if all(is_valid_list):
            break

    return tmsp


def find_earliest_tmsp_for_pattern(bus_lines: List[Tuple[int, int]]) -> int:
    """compute `smarter`"""
    # find numbers that end up on same line due to "multiples" being equal to
    # the offsets -> done in spreadsheet
    same_offsets = [19, 859, 13, 17, 29]
    lcd = math.lcm(*same_offsets)  # Python 3.9 needed for this
    offset = 19

    tmsp_off = 0
    while True:
        tmsp_off += lcd
        tmsp = tmsp_off - offset

        is_valid_list = [(tmsp + idx) % line == 0 for idx, line in bus_lines]
        if all(is_valid_list):
            break

    return tmsp


def main() -> None:
    tta, bus_lines = parse_instructions(utils.get_input(__file__))

    # part 1
    min_wait_hash = find_line_next_depart(tta, bus_lines)
    print(f"part 1: {min_wait_hash}")

    # part 2
    earliest_tmsp = find_earliest_tmsp_for_pattern(bus_lines)
    print(f"part 2: {earliest_tmsp}")


if __name__ == "__main__":
    main()
