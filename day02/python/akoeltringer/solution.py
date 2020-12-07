#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 02"""

# stdlib imports
import collections
from typing import List

# 3rd party lib imports

# own stuff
import utils


class Password:
    pw: str
    letter: str
    lower: int
    upper: int

    def __init__(self, password: str):
        self.parse_pw(password)

    def parse_pw(self, pw: str) -> None:
        pol, pw = pw.split(": ")
        letter_range, letter = pol.split(" ")
        lower, upper = letter_range.split("-")

        self.pw = pw
        self.letter = letter
        self.lower = int(lower)
        self.upper = int(upper)

    def is_valid_old(self):
        counts = collections.Counter(self.pw)
        return True if self.lower <= counts[self.letter] <= self.upper else False

    def is_valid(self):
        return (self.pw[self.lower - 1] == self.letter) != (
            self.pw[self.upper - 1] == self.letter
        )


def get_passwords() -> List[Password]:
    """get the intcodes from the website"""
    return [Password(elem) for elem in utils.get_input(__file__).strip().split("\n")]


def main():
    passwords = get_passwords()

    # part 1
    n_valid_old = sum([pw.is_valid_old() for pw in passwords])
    print(f"valid passwords: {n_valid_old}")

    # part 2
    n_valid = sum([pw.is_valid() for pw in passwords])
    print(f"valid passwords: {n_valid}")


if __name__ == "__main__":
    main()
