#!/usr/bin/env python

import doctest
import logging
import math as m
import re
from networkx import DiGraph
import copy
import itertools as it


def load_input():
    data = list()
    with open('input.txt') as fd:
        for line in fd:
            value = line.strip()
            data.append(value)
    return data

class Board:

    neighbors_dir = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

    def __init__(self, data):
        "docstring"
        self._board = data
        self._size_y = len(data)
        self._size_x = len(data[0])

    def _is_in_range(self, y, x):
        if y >= 0 and y < self._size_y and x >= 0 and x < self._size_x:
            return True
        else:
            return False

    def visible_occupied_part2(self, y, x):
        occupied = 0
        for direction in Board.neighbors_dir:
            y_n = y
            x_n = x
            while True:
                y_n += direction[0]
                x_n += direction[1]
                if not self._is_in_range(y_n, x_n):
                    break
                if self._board[y_n][x_n] == '#':
                    occupied += 1
                    break
                elif self._board[y_n][x_n] == 'L':
                    break
        return occupied

    def visible_occupied_part1(self, y, x):
        neighbors = [[y + i, x + j] for i, j in Board.neighbors_dir]
        occupied = 0
        for neighbor in neighbors:
            if self._is_in_range(neighbor[0], neighbor[1]):
                if self._board[neighbor[0]][neighbor[1]] == '#':
                    occupied += 1
        return occupied

    def update(self, visible_occupied, limit=4):
        updated_board = list()
        change_detected = False

        for y in range(self._size_y):
            row = str()
            for x in range(self._size_x):
                status = self._board[y][x]
                if status != '.':
                    occupied = visible_occupied(y, x)

                    if status == 'L' and occupied == 0:
                        change_detected = True
                        status = '#'

                    elif status == '#' and occupied >= limit:
                        change_detected = True
                        status = 'L'
                    else:
                        pass
                row += status

            updated_board.append(row)

        self._board = updated_board
        return change_detected

    def print_board(self):
        print("")
        for row in self._board:
            print(row)

    def number_occupied(self):
        occupied = 0
        for row in self._board:
            occupied += row.count('#')
        return occupied


def main():
    data = load_input()

    b = Board(data.copy())
    count = 0
    while True:
        count += 1
        if not b.update( b.visible_occupied_part1, 4):
            break
    print("Part1: ", b.number_occupied())

    b = Board(data.copy())
    count = 0
    while True:
        count += 1
        if not b.update( b.visible_occupied_part2, 5):
            break
    print("Part2: ", b.number_occupied())



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
