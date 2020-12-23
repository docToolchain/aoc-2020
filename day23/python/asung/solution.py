#!/usr/bin/env python3
import os
from typing import Dict, Iterator, List


class Solver:
    def __init__(self, filepath: str) -> None:
        with open(filepath, 'r') as text_file:
            self.cups = [int(label) for label in text_file.read().strip()]

    @staticmethod
    def solve(cups: List[int], move_count: int) -> Iterator[int]:
        # Store the successor cup for each cup.
        successors = {}  # type: Dict[int, int]
        last_cup = cups[-1]
        for cup in cups:
            successors[last_cup] = cup
            last_cup = cup
        cup_count = len(cups)
        # Designate the first cup.
        current_cup = cups[0]
        # Do move_count moves.
        for _ in range(move_count):
            # Pick up three cups.
            successor1 = successors[current_cup]
            successor2 = successors[successor1]
            successor3 = successors[successor2]
            successors[current_cup] = successors[successor3]
            # Select destination cup.
            destination_cup = (current_cup - 2) % cup_count + 1
            while destination_cup in {successor1, successor2, successor3}:
                # Wrap around.
                destination_cup = (destination_cup - 2) % cup_count + 1
            # Place picked up cups.
            successors[successor3] = successors[destination_cup]
            successors[destination_cup] = successor1
            # Select new current cup.
            current_cup = successors[current_cup]
        # Start after the cup labeled 1.
        current_cup = 1
        # Collect other cups.
        for _ in range(1, cup_count):
            current_cup = successors[current_cup]
            yield current_cup

    def solve_part1(self) -> int:
        return int(''.join(str(cup) for cup in self.solve(self.cups, 100)))

    def solve_part2(self) -> int:
        cup_count = 1000000
        move_count = 10000000
        cups = self.cups + list(range(len(self.cups) + 1, cup_count + 1))
        results = self.solve(cups, move_count)
        return next(results) * next(results)


if __name__ == "__main__":
    solver = Solver(os.path.join(os.path.dirname(__file__), "input.txt"))
    print(solver.solve_part1())
    print(solver.solve_part2())
