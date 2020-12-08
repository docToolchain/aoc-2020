import doctest
import logging
import math as m
import re
from networkx import DiGraph
import copy


class Console(object):
    def __init__(self, program):
        "docstring"
        self._program = program
        self._size = len(program)
        self._hist = list()
        self._acc = 0
        self._pc = 0

    def _step(self):
        cmd = self._program[self._pc][0]
        data = self._program[self._pc][1]
        self._hist.append(self._pc)

        if cmd == "acc":
            self._acc += data
            self._pc += 1
        elif cmd == "jmp":
            self._pc += data
        elif cmd == "nop":
            self._pc += 1
        else:
            pass
        return

    def run(self):
        ret_part2 = None
        ret_part1 = None

        while True:
            self._step()
            if self._pc in self._hist:
                ret_part1 = self._acc
                break
            if self._pc == self._size:
                ret_part2 = self._acc
                break
        return ret_part1, ret_part2


def load_input():
    data = list()
    with open('input.txt') as fd:
        for line in fd:
            value = line.strip().split()
            data.append([value[0], int(value[1])])
    return data


def main():
    data = load_input()

    cons = Console(data.copy())
    result, _ = cons.run()
    print("Part1: ", result)

    result = None
    for i in range(len(data)):
        mod = copy.deepcopy(data)
        if mod[i][0] == "jmp":
            mod[i][0] = "nop"
        elif mod[i][0] == "nop":
            mod[i][0] = "jmp"
        else:
            continue
        cons = Console(mod)
        _, result = cons.run()
        if result:
            break

    print("Part2: ", result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
