#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 07"""

# stdlib imports
from typing import List, Tuple, Dict

# 3rd party lib imports

# own stuff
import utils

SHINY_GOLD_BAGS = "shiny gold bags"

# types
RuleContent = Tuple[int, str]
Rule = Tuple[str, List[RuleContent]]
RulesDict = Dict[str, List[RuleContent]]


def split_rule_content(elem: str) -> RuleContent:
    """split the `content` of a rule (i.e. the part after the ` contains ` into its
    parts
    """
    elem = elem.strip()
    # normalize quantity
    if elem.endswith("bag"):
        elem = elem.replace("bag", "bags")

    if elem == "no other bags":
        return tuple()

    elems = elem.split(" ", 1)
    return int(elems[0]), elems[1]


def split_rule(rule: str) -> Rule:
    """split the rule into its parts: the container (the part before ` contains `) and
    the contents (the part after ` contains `)"""
    container, contents_str = rule.split(" contain ")
    contents = [
        split_rule_content(elem) for elem in contents_str.replace(".", "").split(",")
    ]

    return container, contents


def parse_rules(rules_raw: str) -> RulesDict:
    """parse the rules and create a dictionary from them"""
    return {k: v for k, v in map(split_rule, rules_raw.strip().split("\n"))}


def find_containers(rules: RulesDict, what: str) -> List[str]:
    """find containers that contain `what` on all paths (result may contain duplicates)
    """
    keys = []
    for key, value in rules.items():
        if what in [bag[1] for bag in value if len(bag) > 0]:
            keys += find_containers(rules, key) + [key]

    return keys


def count_distinct_containers(rules: RulesDict, what: str) -> int:
    """count the distinct containers that were found by `find_containers`"""
    return len(set(find_containers(rules, what)))


def count_bags_within(rules: RulesDict, what: str) -> int:
    """count the bags located within a bag"""
    n_bags = 0
    for elem in rules.get(what, []):
        if len(elem) == 0:
            continue

        # the number is stored in the first location, the name in the second
        # like so: (4, "muted yellow bags")
        n_bags += elem[0] * (count_bags_within(rules, elem[1]) + 1)

    return n_bags


def main() -> None:
    rules_raw = utils.get_input(__file__)
    rules = parse_rules(rules_raw)

    # part 1
    n_containers = count_distinct_containers(rules, SHINY_GOLD_BAGS)
    print(f"part 1: number containers:  {n_containers}")

    # part 2
    n_bags_within = count_bags_within(rules, SHINY_GOLD_BAGS)
    print(f"part 2: number of bags within: {n_bags_within}")


if __name__ == "__main__":
    main()
