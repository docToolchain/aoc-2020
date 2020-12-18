#!/usr/bin/env python3
import math
import os
import re


class Puzzle:
    def __init__(self, filepath: str) -> None:
        """Read input file at filepath as a list of stripped strings."""
        with open(filepath, 'r') as text_file:
            self.lines = [line.rstrip() for line in text_file.readlines()]

    @staticmethod
    def apply(operator: str, operand1: int, operand2: int) -> str:
        """Return result of operator applied on operand1 and operand2."""
        if operator == '+':
            return str(operand1 + operand2)

        if operator == '*':
            return str(operand1 * operand2)

        raise NotImplementedError("Invalid operator: {operator}")

    @classmethod
    def different_math(cls, line: str) -> str:
        # First recursively resolve terms in parantheses.
        while ')' in line:
            right_index = line.index(')')
            left_index = line.rindex('(', 0, right_index)
            line = line[:left_index] + cls.different_math(line[left_index+1:right_index]) + line[right_index+1:]
        # Split remaining sequence and apply operators sequentially.
        tokens = line.split()
        while len(tokens) > 1:
            tokens = [cls.apply(tokens[1], int(tokens[0]), int(tokens[2]))] + tokens[3:]
        return "".join(tokens)

    @classmethod
    def advanced_math(cls, line: str) -> str:
        # First recursively resolve terms in parantheses.
        while ')' in line:
            right_index = line.index(')')
            left_index = line.rindex('(', 0, right_index)
            line = line[:left_index] + cls.advanced_math(line[left_index+1:right_index]) + line[right_index+1:]
        # Then resolve additions.
        while '+' in line:
            # Match any * and their left-sided operands, followed by + and its operands, then the rest.
            match_result = re.match(r'((?:\d+\s*\*\s*)*)(\d+)\s*\+\s*(\d+)([\d\s\+\*]*)', line)
            if match_result:
                line = match_result.group(1) + str(int(match_result.group(2)) + int(match_result.group(3))) + match_result.group(4)
            else:
                raise ArithmeticError(f"Cannot parse: {line}")
        # Finally resolve multiplications.
        tokens = line.split()
        return str(math.prod(int(token) for index, token in enumerate(tokens) if index % 2 == 0))

    def solve_part1(self) -> int:
        return sum(int(self.different_math(line)) for line in self.lines)

    def solve_part2(self) -> int:
        return sum(int(self.advanced_math(line)) for line in self.lines)


if __name__ == "__main__":
    solver = Puzzle(os.path.join(os.path.dirname(__file__), "input.txt"))
    print(solver.solve_part1())
    print(solver.solve_part2())
