#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 17"""

# stdlib imports
import copy
import itertools
from typing import Generator, Iterable, Set, Tuple

# 3rd party lib imports

# own stuff
import utils


T_INDEX = Tuple[int, ...]
T_SPARSE_ARRAY = Set[T_INDEX]

ACTIVE = "#"


def parse_input(input_raw: str, n_dims: int) -> T_SPARSE_ARRAY:
    """parse the input and account for "extra dimensions" (input data is a slice
    of the multidimensional qube), e.g. 3 x 3 x 1 x 1
    """
    if n_dims < 2:
        raise ValueError("dimension cannot be smaller than 2")

    extra_idx = (0,) * (n_dims - 2)
    data = set()

    for y, row in enumerate(input_raw.strip().split("\n")):
        for x, col in enumerate(row):
            if col == ACTIVE:
                data.add((x, y) + extra_idx)

    return data


def get_neighbors(idx: Tuple[int, ...]) -> Generator[T_INDEX, None, None]:
    """get the neighbors of a point. warning: contains the point itself"""
    for neighbor in itertools.product(*[range(iv - 1, iv + 2) for iv in idx]):
        if neighbor != idx:
            yield neighbor


def get_index_range(index_values: Iterable[int]) -> range:
    """compute the range of index values for a certain dimension."""
    return range(min(index_values) - 1, max(index_values) + 2)


def compute_cycle(pocket_dimension: T_SPARSE_ARRAY) -> T_SPARSE_ARRAY:
    """compute a single cycle of the boot process. The number of dimensions is
    determined from the data.
    """
    n_dims = len(next(iter(pocket_dimension)))  # get single element from set
    new_pocket_dimension = copy.deepcopy(pocket_dimension)

    def iterate_over_dim(idx: Tuple[int, ...]):
        val_range = get_index_range([p[len(idx)] for p in pocket_dimension])

        for iv in val_range:
            current_idx = idx + (iv,)
            if len(current_idx) == n_dims:
                neighbors = set(get_neighbors(current_idx))
                num_active = len(pocket_dimension.intersection(neighbors))
                if current_idx in pocket_dimension and num_active not in [2, 3]:
                    new_pocket_dimension.remove(current_idx)
                if current_idx not in pocket_dimension and num_active == 3:
                    new_pocket_dimension.add(current_idx)
            else:
                iterate_over_dim(current_idx)

    iterate_over_dim(tuple())

    return new_pocket_dimension


def main() -> None:
    input_raw = utils.get_input(__file__)

    # part 1
    pocket_dim = parse_input(input_raw, 3)
    for _ in range(6):
        pocket_dim = compute_cycle(pocket_dim)
    n_active = len(pocket_dim)
    print(f"part 1: {n_active}")

    # part 2
    pocket_dim = parse_input(input_raw, 4)
    for _ in range(6):
        pocket_dim = compute_cycle(pocket_dim)
    n_active = len(pocket_dim)
    print(f"part 2: {n_active}")


if __name__ == "__main__":
    main()
