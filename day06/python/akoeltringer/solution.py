#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 06"""

# stdlib imports
from typing import List

# 3rd party lib imports

# own stuff
import utils


def get_input() -> List[str]:
    """get input from the website"""
    return utils.get_input(__file__).strip().split("\n\n")


def count_any_question_yes(group_input: str) -> int:
    """count questions any group member answered with yes"""
    return len(set("".join([line.strip() for line in group_input.split("\n")])))


def count_all_questions_yes(group_input: str) -> int:
    """count questions all group members answered with yes"""
    list_of_sets = [set(line.strip()) for line in group_input.split("\n")]
    return len(set.intersection(*list_of_sets))


def main() -> None:
    # make list b/c is being used twice
    groups_data = get_input()

    # part 1
    sum_any_counts = sum(map(count_any_question_yes, groups_data))
    print(f"part 1: sum any counts:  {sum_any_counts}")

    # part 2
    sum_all_counts = sum(map(count_all_questions_yes, groups_data))
    print(f"part 2: sum all counts:  {sum_all_counts}")


if __name__ == "__main__":
    main()
