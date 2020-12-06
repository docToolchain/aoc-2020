#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 05"""

# stdlib imports
from typing import List, Tuple

# 3rd party lib imports

# own stuff
import utils


def get_input() -> List[str]:
    """get input from the website"""
    return utils.get_input(__file__).strip().split("\n")


def zone_to_seat(zone: str) -> Tuple[int, int]:
    """convert the zone code into a seat number given by (row, col)"""
    replacements = [("F", "0"), ("B", "1"), ("L", "0"), ("R", "1")]
    for old, new in replacements:
        zone = zone.replace(old, new)

    return int(zone[:7], base=2), int(zone[7:], base=2)


def get_seat_id(seat: Tuple[int, int]) -> int:
    """calculate seat_id from (row, col)"""
    return seat[0] * 8 + seat[1]


def find_seat_id(seat_ids: List[int]) -> int:
    """find seat id given on the fact that the seats before (-1) and after (+1) are
    in the list
    """
    for seat_id in range(min(seat_ids) + 1, max(seat_ids)):
        if (
            (seat_id - 1) in seat_ids
            and seat_id not in seat_ids
            and (seat_id + 1) in seat_ids
        ):
            return seat_id

    raise RuntimeError("seat id not found")


def main() -> None:
    # make list b/c is being used twice
    zones = get_input()
    seats = [zone_to_seat(zone) for zone in zones]
    seat_ids = [get_seat_id(seat) for seat in seats]

    # part 1
    print(f"part 1: max seat id:  {max(seat_ids)}")

    # part 2
    print(f"part 2: seat id is: {find_seat_id(seat_ids)}")


if __name__ == "__main__":
    main()
