#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 16"""

# stdlib imports
import collections
import dataclasses
import math
from typing import Dict, DefaultDict, List, Tuple

# 3rd party lib imports

# own stuff
import utils


T_MATCHES = Dict[int, List[str]]
T_RULES = List["Rule"]
T_TICKET = List[int]


@dataclasses.dataclass
class Rule:
    name: str
    _parts: List[range]

    def is_valid(self, num: int) -> bool:
        return any([num in part for part in self._parts])


def parse_rules(rules_raw: str) -> T_RULES:
    """parse the rules data"""
    rules = []
    for rule in rules_raw.split("\n"):
        name, body = rule.split(": ")
        body_groups = body.split(" or ")

        rule_parsed = []
        for group in body_groups:
            l, u = group.split("-")
            rule_parsed.append(range(int(l), int(u) + 1))

        rules.append(Rule(name, rule_parsed))

    return rules


def parse_tickets(tickets_raw: str) -> List[T_TICKET]:
    """parse the ticket fields (omit first line)"""
    tickets = []
    for ticket in tickets_raw.split("\n")[1:]:
        tickets.append([int(num) for num in ticket.split(",")])

    return tickets


def parse_input(input_raw: str) -> Tuple[T_RULES, T_TICKET, List[T_TICKET]]:
    """parse the input data"""
    rules_raw, my_ticket_raw, other_tickets_raw = input_raw.strip().split("\n\n")
    return (
        parse_rules(rules_raw),
        parse_tickets(my_ticket_raw)[0],
        parse_tickets(other_tickets_raw),
    )


def is_valid_any(num: int, rules: T_RULES) -> bool:
    """check if a field value is valid for at least one rule"""
    for rule in rules:
        if rule.is_valid(num):
            return True

    return False


def find_valid_tickets(
    rules: T_RULES, tickets: List[T_TICKET]
) -> Tuple[List[T_TICKET], List[int]]:
    """find valid tickets, i.e. remove tickets with fields that match none of the rules
    from the list.
    """
    invalid_nums = []
    valid_tickets = []

    for ticket in tickets:
        ticket_valid = True
        for num in ticket:
            if not is_valid_any(num, rules):
                invalid_nums.append(num)
                ticket_valid = False

        if ticket_valid:
            valid_tickets.append(ticket)

    return valid_tickets, invalid_nums


def find_matching_rules(rules: T_RULES, tickets: List[T_TICKET]) -> T_MATCHES:
    """get all values for a field and find the rules that match all the values."""
    matches: DefaultDict[int, List[str]] = collections.defaultdict(list)

    for field_num in range(len(tickets[0])):
        field_values = [t[field_num] for t in tickets]
        for r in rules:
            if all([r.is_valid(v) for v in field_values]):
                matches[field_num] += [r.name]

    return matches


def find_assignments(matches: T_MATCHES) -> Dict[int, str]:
    """start assigning fields by the number of matches each field has. If there is
    only one matching field left, directly assign. If not, raise an error.
    """
    items = sorted(matches, key=lambda x: len(matches[x]))
    result: Dict[int, str] = {}

    for item in items:
        remaining_fields = set(matches[item]).difference(result.values())
        if len(remaining_fields) == 1:
            result[item] = remaining_fields.pop()
        else:
            print(item, remaining_fields)
            raise ValueError("more than one remaining field")

    return result


def get_product_departure_values(
    rules: T_RULES, tickets: List[T_TICKET], my_ticket: T_TICKET
) -> int:
    """find the field for each position. return the product of all "departure" fields
    of "my" ticket.
    """
    valid_tickets = tickets + [my_ticket]
    matches = find_matching_rules(rules, valid_tickets)
    assignments = find_assignments(matches)
    departure_values = [
        my_ticket[idx]
        for idx, val in assignments.items()
        if val.startswith("departure")
    ]
    return math.prod(departure_values)


def main() -> None:
    rules, my_ticket, other_tickets = parse_input(utils.get_input(__file__))

    # part 1
    valid_tickets, invalid_values = find_valid_tickets(rules, other_tickets)
    print(f"part 1: {sum(invalid_values)}")

    # part 2
    product_departure_values = get_product_departure_values(
        rules, valid_tickets, my_ticket
    )
    print(f"part 2: {product_departure_values}")


if __name__ == "__main__":
    main()
