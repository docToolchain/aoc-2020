#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 21"""

# stdlib imports
import copy
import functools
from typing import Dict, List, Set, Tuple

# 3rd party lib imports

# own stuff
import utils


def parse_input(input_raw: str) -> Tuple[List[str], Dict[str, Set[str]]]:
    a2i: Dict[str, Set[str]] = {}
    ingredients: List[str] = []

    for line in input_raw.strip().split("\n"):
        line = line.replace(")", "")
        ingredients_raw, allergens_raw = line.split(" (contains ")

        i = ingredients_raw.split(" ")
        ingredients += i

        a = allergens_raw.split(", ")
        for elem in a:
            a2i[elem] = a2i[elem].intersection(i) if elem in a2i else set(i)

    return ingredients, a2i


def get_ingredients_without_allergenes(
    ingredients: List[str], a2i: Dict[str, Set[str]]
) -> int:
    i_with_a = functools.reduce(set.union, a2i.values())
    return sum(i not in i_with_a for i in ingredients)


def map_allergenes_to_ingredients(a2i: Dict[str, Set[str]]) -> str:
    a2i = copy.deepcopy(a2i)
    i2a: Dict[str, str] = {}

    while len(a2i) > 0:
        a = min(a2i, key=lambda x: len(a2i[x]))

        candidates = a2i[a].difference(i2a)
        if len(candidates) != 1:
            raise ValueError("more than one candiate left")

        candidate = next(iter(candidates))
        i2a[candidate] = a

        for v in a2i.values():
            try:
                v.remove(candidate)
            except KeyError:
                pass

        del a2i[a]

    return ",".join(sorted(i2a, key=lambda x: i2a[x]))


def main() -> None:
    input_raw = utils.get_input(__file__)
    ingredients, a2i = parse_input(input_raw)

    num_i_without_a = get_ingredients_without_allergenes(ingredients, a2i)
    print(f"part 1: {num_i_without_a}")

    ingredients_by_allergene = map_allergenes_to_ingredients(a2i)
    print(f"part 2: {ingredients_by_allergene}")


if __name__ == "__main__":
    main()
