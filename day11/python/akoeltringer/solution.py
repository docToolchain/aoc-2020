#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 10"""

# stdlib imports
import copy
import itertools
from typing import Callable, Generator, Iterable, List, Optional, Tuple, TypeVar

# 3rd party lib imports

# own stuff
import utils

T = TypeVar("T")
T_GRID = List[List[str]]

S_SEAT_EMPTY = "L"
S_FLOOR = "."
S_SEAT_OCCUPIED = "#"


def parse_grid(input_raw: str) -> T_GRID:
    return [list(row) for row in input_raw.strip().split("\n")]


def get_neighbor_coords(y, x, height, width) -> Tuple[int, int, int, int]:
    """get the neighbor indices: min/max row and min/max col"""
    if 0 > y > height or 0 > x > width:
        raise ValueError("x/y need to be between 0 and width/height")

    y_lower = max(y - 1, 0)
    y_upper = min(y + 1, height - 1)  # highest index is height - 1
    x_lower = max(x - 1, 0)
    x_upper = min(x + 1, width - 1)  # highest index is width - 1

    return y_lower, y_upper, x_lower, x_upper


def get_neighboring_elements(
    grid: List[List[T]], y_pos: int, x_pos: int
) -> Generator[T, None, None]:
    """get the neighboring elements"""
    height, width = len(grid), len(grid[0])
    y_lower, y_upper, x_lower, x_upper = get_neighbor_coords(
        y_pos, x_pos, height, width
    )

    for y in range(y_lower, y_upper + 1):
        for x in range(x_lower, x_upper + 1):
            if x == x_pos and y == y_pos:
                continue

            yield grid[y][x]


def count_occupied(neighbors: Iterable[str]) -> int:
    """count how many seats are occupied"""
    return sum([1 for elem in neighbors if elem == S_SEAT_OCCUPIED])


def compute_round_1(grid: T_GRID) -> T_GRID:
    """apply one round of changes to the grid"""
    grid_new = copy.deepcopy(grid)
    height, width = len(grid), len(grid[0])

    for y in range(height):
        for x in range(width):
            neighbors = list(get_neighboring_elements(grid, y, x))
            n_occupied = count_occupied(neighbors)

            if grid[y][x] == S_SEAT_EMPTY and n_occupied == 0:
                grid_new[y][x] = S_SEAT_OCCUPIED

            if grid[y][x] == S_SEAT_OCCUPIED and n_occupied >= 4:
                grid_new[y][x] = S_SEAT_EMPTY

    return grid_new


def get_diag_1(
    grid: List[List[T]], y_pos: int, x_pos: int
) -> Generator[Optional[T], None, None]:
    """get upper/left to lower/right diagonal

    Note: the placements are y-aligned -> y_pos determines the current element in the
    returned sequence of elements
    """
    height, width = len(grid), len(grid[0])
    x_start = x_pos - y_pos

    for y in range(height):
        x = x_start + y

        if x < 0 or x >= width:
            yield None
            continue

        yield grid[y][x]


def get_diag_2(
    grid: List[List[T]], y_pos: int, x_pos: int
) -> Generator[Optional[T], None, None]:
    """get upper/right to lower/left diagonal

    Note: the placements are y-aligned -> y_pos determines the current element in the
    returned sequence of elements
    """
    height, width = len(grid), len(grid[0])
    x_start = x_pos + y_pos

    for y in range(height):
        x = x_start - y

        if x < 0 or x >= width:
            yield None
            continue

        yield grid[y][x]


def is_occupied(ahead: Iterable[Optional[str]]) -> bool:
    for elem in ahead:
        if elem in [S_SEAT_EMPTY, S_SEAT_OCCUPIED]:
            return elem == S_SEAT_OCCUPIED

    return False


def compute_round_2(grid: T_GRID) -> T_GRID:
    """apply one round of changes to the grid (rules of round 2)"""
    grid_new = copy.deepcopy(grid)
    height, width = len(grid), len(grid[0])

    for y in range(height):
        for x in range(width):
            row = grid[y]
            col = [elem[x] for elem in grid]
            diag1 = list(get_diag_1(grid, y, x))
            diag2 = list(get_diag_2(grid, y, x))

            left = is_occupied(reversed(row[:x]))
            right = is_occupied(row[(x + 1) :])
            up = is_occupied(reversed(col[:y]))
            down = is_occupied(col[(y + 1) :])
            left_up = is_occupied(reversed(diag1[:y]))
            right_down = is_occupied(diag1[(y + 1) :])
            right_up = is_occupied(reversed(diag2[:y]))
            left_down = is_occupied(diag2[(y + 1) :])

            n_occupied = sum(
                [left, right, up, down, left_up, right_down, right_up, left_down]
            )

            if grid[y][x] == S_SEAT_EMPTY and n_occupied == 0:
                grid_new[y][x] = S_SEAT_OCCUPIED

            if grid[y][x] == S_SEAT_OCCUPIED and n_occupied >= 5:
                grid_new[y][x] = S_SEAT_EMPTY

    return grid_new


def compute_rounds(grid: T_GRID, compute_fun: Callable[[T_GRID], T_GRID]) -> int:
    """iterate the rules until an equilibrium is found"""

    changed = False
    while not changed:

        grid_new = compute_fun(grid)
        changed = grid == grid_new
        grid = grid_new

    return count_occupied(itertools.chain(*grid))


def main() -> None:
    grid = parse_grid(utils.get_input(__file__))

    # part 1
    n_occupied_1 = compute_rounds(grid, compute_round_1)
    print(f"part 1: {n_occupied_1}")

    # part 2
    n_occupied_2 = compute_rounds(grid, compute_round_2)
    print(f"part 2: {n_occupied_2}")


if __name__ == "__main__":
    main()
