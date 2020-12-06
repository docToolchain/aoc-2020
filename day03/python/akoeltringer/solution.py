#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 03"""

# stdlib imports
import math
from typing import List

# 3rd party lib imports

# own stuff
import utils


S_TREE = "#"
S_OPEN_SQUARE = "."


def get_grid() -> List[str]:
    """get input from the website"""
    return utils.get_input(__file__).strip().split("\n")


def walk_count_trees(del_x: int, del_y: int, grid: List[str]) -> int:
    """walk the grid and count the trees along the way."""
    x_width = len(grid[0])
    x_pos = -del_x
    n_trees = 0
    for j in range(0, len(grid), del_y):
        x_pos = (x_pos + del_x) % x_width

        if grid[j][x_pos] == S_TREE:
            n_trees += 1
        elif grid[j][x_pos] == S_OPEN_SQUARE:
            pass
        else:
            raise ValueError

    return n_trees


def main() -> None:
    grid = get_grid()

    # part 1
    n_trees = walk_count_trees(3, 1, grid)
    print(f"part 1: trees encountered: {n_trees}")

    # part 2
    steps = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    n_trees_list = []
    for right, down in steps:
        n_trees_list.append(walk_count_trees(right, down, grid))

    print(f"part 2: prod of trees encountered: {math.prod(n_trees_list)}")


if __name__ == "__main__":
    main()
