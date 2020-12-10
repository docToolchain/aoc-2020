#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 08"""

# stdlib imports
import copy
from typing import List, Tuple

# 3rd party lib imports

# own stuff
import utils


def parse_instruction(instruction: str) -> Tuple[str, int]:
    """parse a single instruction"""
    instr_tup = instruction.split(" ")
    return instr_tup[0], int(instr_tup[1])


def parse_instructions(instructions_str: str) -> List[Tuple[str, int]]:
    """parse the input (instructions)"""
    return [parse_instruction(elem) for elem in instructions_str.strip().split("\n")]


def debug_instructions(instructions: List[Tuple[str, int]], instr_visited: List[int]):
    """debug instructions, i.e. replace one jmp/nop instruction with the other"""
    # find last used instruction that was either jmp or nop and change
    for i in instr_visited:
        name, param = instructions[i]
        if name in ["jmp", "nop"]:
            instr_new = copy.deepcopy(instructions)
            new_name = "jmp" if name == "nop" else "nop"
            instr_new[i] = (new_name, param)

            acc, rc = computer(instr_new)
            if rc == 0:
                print(f"normal termination, acc was {acc}")


def computer(
    instructions: List[Tuple[str, int]], debug: bool = False
) -> Tuple[int, int]:
    """instructions computer"""

    rc = 0
    accumulator = 0
    instr_pointer = 0
    instr_visited: List[int] = []

    while True:
        if instr_pointer >= len(instructions):
            break

        if instr_pointer in instr_visited:
            if debug:
                debug_instructions(instructions, instr_visited)

            rc = -1
            break

        instr_name, instr_param = instructions[instr_pointer]
        instr_visited.append(instr_pointer)

        if instr_name == "nop":
            pass

        elif instr_name == "acc":
            accumulator += instr_param

        elif instr_name == "jmp":
            instr_pointer += instr_param
            continue

        instr_pointer += 1

    return accumulator, rc


def main() -> None:
    instructions = parse_instructions(utils.get_input(__file__))

    # part 1
    acc_before = computer(instructions)
    print(f"part 1: accumulator before:  {acc_before}")

    # part 2
    acc_term = computer(instructions, debug=True)
    print(f"part 2: accumulator after 2nd part:  {acc_term}")


if __name__ == "__main__":
    main()
