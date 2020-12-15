#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 14"""

# stdlib imports
import re
from typing import List, Callable

# 3rd party lib imports

# own stuff
import utils


MEM_PATTERN = re.compile(r"^mem\[([0-9]+)\] = ([0-9]+)$")


def get_apply_mask_value_func(mask_raw: str) -> Callable[[int], int]:
    """create function that does value translation"""
    mask_to_one = int(mask_raw.replace("X", "0"), base=2)
    mask_to_zero = int(mask_raw.replace("X", "1"), base=2)

    def apply_mask_func(num: int) -> int:
        return (num & mask_to_zero) | mask_to_one

    return apply_mask_func


def value_decoder(instructions: List[str]) -> int:
    """run the value decoder"""
    apply_mask_func = lambda x: x
    memory = {}

    for instruction in instructions:
        if instruction.startswith("mask = "):
            mask = instruction[7:]
            apply_mask_func = get_apply_mask_value_func(mask)

        else:
            elems = MEM_PATTERN.fullmatch(instruction)
            if elems is None:
                raise ValueError
            idx, val = int(elems.group(1)), int(elems.group(2))

            memory[idx] = apply_mask_func(val)

    return sum(memory.values())


def get_apply_mask_addr_func(mask_raw: str) -> Callable[[int], List[int]]:
    """create function that does memory address translation"""
    mask_to_one = int(mask_raw.replace("X", "0"), base=2)

    def apply_mask_func(addr: int) -> List[int]:
        addr = addr | mask_to_one
        # put "{}" into the bit representation where the 'X' in the masks are
        # results in a string like "000{}1" which can be formatted afterwards:
        # "000{}1".format()
        addr_str = "".join(
            n if m != "X" else "{}" for n, m in zip(f"{addr:036b}", mask_raw)
        )
        n_repl = addr_str.count("{}")
        # - if there are n "X" in the string, this allows for 2 ** n combinations
        # - loop over range(0, n), get the bit representation of the number with
        #   leading zeros (such that the resulting string is n chars long):
        #       f"{i:0{n_repl}b}"
        # - explode the string into a list of characters and feed them as format inputs
        #   into the address string.
        # - convert to int afterwards.
        return [
            int(addr_str.format(*list(f"{i:0{n_repl}b}")), base=2)
            for i in range(2 ** n_repl)
        ]

    return apply_mask_func


def memory_address_decoder(instructions: List[str]) -> int:
    """run the memory address decoder"""
    memory = {}

    for instruction in instructions:
        if instruction.startswith("mask = "):
            mask = instruction[7:]
            apply_mask_func = get_apply_mask_addr_func(mask)

        else:
            elems = MEM_PATTERN.fullmatch(instruction)
            if elems is None:
                raise ValueError

            idx, val = int(elems.group(1)), int(elems.group(2))

            for address in apply_mask_func(idx):
                memory[address] = val

    return sum(memory.values())


def main() -> None:
    instructions = [x for x in utils.get_input(__file__).strip().split("\n")]

    # part 1
    sum_mem_vals = value_decoder(instructions)
    print(f"part 1: {sum_mem_vals}")

    # part 2
    sum_mem_vals = memory_address_decoder(instructions)
    print(f"part 2: {sum_mem_vals}")


if __name__ == "__main__":
    main()
