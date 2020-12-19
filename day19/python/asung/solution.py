#!/usr/bin/env python3
import os
from functools import lru_cache
from typing import Dict, List, Set


class Solution:
    def __init__(self, filepath: str) -> None:
        """Read rules and messages from file."""
        with open(filepath, 'r') as text_file:
            groups = text_file.read().split('\n\n')
            self.rules = {}  # type: Dict[str, List[str]]
            for line in groups[0].split('\n'):
                precondition, action = line.split(": ", maxsplit=1)
                self.rules[precondition] = action.split(" | ")
            self.messages = groups[-1].split('\n')

    @staticmethod
    def apply_rule8_fix(options: Set[str], message: str) -> List[str]:
        """Return all possible parts of message after fulfilling fixed rule 8."""
        part_length = len(next(iter(options)))
        for option in options:
            assert len(option) == part_length, "Options of rule 42 do not all have same length."

        parts = []  # type: List[str]
        while len(message) > part_length:
            if message[:part_length] in options:
                message = message[part_length:]
                parts.append(message)
            else:
                break

        return parts

    @staticmethod
    def check_rule11_fix(options_left: Set[str], message_part: str, options_right: Set[str]) -> bool:
        """Return whether message_part fulfills fixed rule 11."""
        part_left_length = len(next(iter(options_left)))
        part_right_length = len(next(iter(options_right)))
        parts_total_length = part_left_length + part_right_length
        for option in options_right:
            assert len(option) == part_right_length, "Options of rule 31 do not all have same length."

        while message_part:
            if len(message_part) < parts_total_length or message_part[:part_left_length] not in options_left \
                    or message_part[-part_right_length:] not in options_right:
                return False

            message_part = message_part[part_left_length:-part_right_length]
        return True

    @lru_cache
    def resolve_action(self, action: str) -> Set[str]:
        """Resolve right-hand side of a rule by recursively applying the rules and composing all combinations."""
        if action.startswith('"') and action.endswith('"'):
            return {action[1:-1]}

        preconditions = action.split(' ')
        sub_actions = {''}
        for precondition in preconditions:
            sub_actions = {sub_action + option for sub_action in sub_actions
                for option in self.calculate_options(precondition)}
        return sub_actions

    @lru_cache
    def calculate_options(self, precondition: str) -> Set[str]:
        """Resolve left-hand side of a rule by resolving all its right-hand side options."""
        options = set()  # type: Set[str]
        for sub_action in self.rules[precondition]:
            options.update(self.resolve_action(sub_action))
        return options

    def solve_part1(self) -> int:
        options = self.calculate_options('0')
        return sum([1 for message in self.messages if message in options])

    def solve_part2(self) -> int:
        assert self.rules['0'] == ["8 11"], "Rule 0 does not compose 8 and 11 as assumed."
        options31 = self.calculate_options('31')
        options42 = self.calculate_options('42')
        result = 0
        for message in self.messages:
            remaining_parts = self.apply_rule8_fix(options42, message)  # 8: 42 | 42 8
            for remaining_part in remaining_parts:
                if self.check_rule11_fix(options42, remaining_part, options31):  # 11: 42 31 | 42 11 31
                    result += 1
                    break
        return result


if __name__ == "__main__":
    solver = Solution(os.path.join(os.path.dirname(__file__), "input.txt"))
    print(solver.solve_part1())
    print(solver.solve_part2())
