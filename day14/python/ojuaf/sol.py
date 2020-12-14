#!/usr/bin/env python

import doctest
import logging
import re
import itertools as it


def load_input():
    program = list()
    pattern = re.compile("mem\[([^\]]+)\].*")
    with open('input.txt') as fd:
        for line in fd:
            command = list()
            value = list(map(lambda x: x.strip(), line.strip().split("=")))
            if value[0].startswith("mem"):
                match = pattern.search(value[0])
                command = ["mem", [int(match.group(1)), int(value[1])]]
            elif value[0].startswith("mask"):
                command = ["mask", list(value[1])]
            else:
                print("OH NO!")
            program.append(command)
    return program


class Computer(object):
    def __init__(self, program):
        "docstring"
        self._program = program
        self._mask = list("0"*36)
        self.memory = dict()

    def _calc_address(self, address):
        raise NotImplemented("Function not implemented!")

    def _calc_value(self, value):
        raise NotImplemented("Function not implemented!")

    def inititialize(self):
        for command in self._program:
            if command[0] == "mem":
                address = command[1][0]
                value = command[1][1]

                addresses = self._calc_address(address)
                value = self._calc_value(value)

                for i in addresses:
                    self.memory[i] = value

            elif command[0] == "mask":
                self._mask = command[1]
            else:
                print("OH NO!")
        return


class ComputerPart2(Computer):
    def __init__(self, program):
        "docstring"
        super().__init__(program)

    def _calc_address(self, address):
        """"""
        address = bin(address)[2:]
        zeros = 36 - len(address)
        address = zeros*"0" + address

        addresses = list()

        masked_address = [y if y == "X" or y == '1' else x for  x, y in zip(address, self._mask)]
        nbr_x = "".join(masked_address).count('X')
        pos = [i for i in range(len(masked_address)) if masked_address[i] == 'X']
        for digits in it.product(('0', '1'), repeat=nbr_x):
            for i, j in enumerate(pos):
                masked_address[j] = digits[i]
            addresses.append(int("".join(masked_address), 2))

        return addresses

    def _calc_value(self, value):
        """"""
        return value


class ComputerPart1(Computer):
    def __init__(self, program):
        "docstring"
        super().__init__(program)

    def _calc_address(self, address):
        """"""
        addresses = [address]
        return addresses

    def _calc_value(self, value):
        """"""
        value = bin(value)[2:]
        zeros = 36 - len(value)
        value = zeros*"0" + value
        masked_value = [x if y == "X" else y for x, y in zip(value, self._mask)]
        value = int("".join(masked_value), 2)
        return value


def main():
    program = load_input()

    comp = ComputerPart1(program)
    comp.inititialize()
    result = sum(comp.memory.values())
    print("Part1: ", result)

    comp = ComputerPart2(program)
    comp.inititialize()
    result = sum(comp.memory.values())
    print("Part2: ", result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
