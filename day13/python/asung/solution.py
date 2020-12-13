#!/usr/bin/env python3
import math
import os
from typing import List, Tuple


class Puzzle:
    def __init__(self, filepath: str) -> None:
        # Read input file at filepath as a list of stripped strings.
        with open(filepath, 'r') as text_file:
            self.lines = [line.rstrip() for line in text_file.readlines()]

    @classmethod
    def use_extended_euclidean_algorithm(cls, a: int, b: int) -> Tuple[int, int]:
        """
        Apply the Extended Euclidean algorithm as described at:
            https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
        """
        if b == 0:
            return (1, 0)

        s, t = cls.use_extended_euclidean_algorithm(b, a % b)
        return (t, s - (a // b) * t)

    @classmethod
    def use_chinese_remainder_theorem(cls, congruences: List[Tuple[int, int]]) -> int:
        """
        Apply the Chinese remainder theorem as described at:
            https://en.wikipedia.org/wiki/Chinese_remainder_theorem
        """
        product = math.prod([divisor for divisor, _ in congruences])
        solution = 0
        for divisor, remainder in congruences:
            product_by_divisor = product // divisor
            r, s = cls.use_extended_euclidean_algorithm(divisor, product_by_divisor)
            assert r * divisor + s * product_by_divisor == 1
            e = s * product_by_divisor
            for check_divisor, _ in congruences:
                assert e % check_divisor == (1 if check_divisor == divisor else 0)
            solution += remainder * e
        return solution % product

    def solve_part1(self) -> int:
        timestamp = int(self.lines[0])
        bus_ids = [int(bus_id) for bus_id in self.lines[1].split(',') if bus_id !='x']
        earliest_departures = [bus_id * ((timestamp - 1) // bus_id + 1) for bus_id in bus_ids]
        earliest_departure = min(earliest_departures)
        earliest_bus_id = bus_ids[earliest_departures.index(earliest_departure)]
        min_wait = earliest_departure - timestamp
        return earliest_bus_id * min_wait

    def solve_part2(self) -> int:
        bus_ids = [int(bus_id) if bus_id != 'x' else None for bus_id in self.lines[-1].split(',')]
        # Note: Assuming all bus_ids are primes.
        congruences = [(bus_id, bus_id - index) for index, bus_id in enumerate(bus_ids) if bus_id]
        return self.use_chinese_remainder_theorem(congruences)


if __name__ == "__main__":
    solver = Puzzle(os.path.join(os.path.dirname(__file__), "input.txt"))
    print(solver.solve_part1())
    print(solver.solve_part2())
