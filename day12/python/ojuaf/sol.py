#!/usr/bin/env python

import doctest
import logging
import math as m
import re
from networkx import DiGraph
import copy
import itertools as it
import numpy as np


def load_input():
    data = list()
    with open('input.txt') as fd:
        for line in fd:
            value = line.strip()
            direction = value[0]
            distance = int(value[1:])
            step = [direction, distance]
            data.append(step)
    return data


class Direction:
    UP    = 0
    RIGHT = 1
    DOWN  = 2
    LEFT  = 3
    COORDS = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])
    FORWARD  = 4


class Board(object):
    """"""
    def __init__(self, data, ship):
        """"""
        self._ship = ship
        self._data = data

    def start(self):
        for step in self._data:
            direction = step[0]
            value = step[1]

            direct = None
            if direction == 'R':
                self._ship.turn_right(value)
            elif direction == 'L':
                self._ship.turn_left(value)
            elif direction == 'N':
                direct = Direction.UP
            elif direction == 'E':
                direct = Direction.RIGHT
            elif direction == 'S':
                direct = Direction.DOWN
            elif direction == 'W':
                direct = Direction.LEFT
            elif direction == 'F':
                direct = Direction.FORWARD
            else:
                print("OH NO!")

            if direct is not None:
                self._ship.move_forward(value, direct)

        return self.manhattan_distance(np.array([0, 0]), self._ship.get_pos())

    def manhattan_distance(self, pos0, pos1):
        return abs(pos0[0] - pos1[0]) + abs(pos0[1] - pos1[1])


class Ship(object):
    def turn_left(self, degree):
        raise NotImplementedError("Not implemented!")

    def turn_right(self, degree):
        raise NotImplementedError("Not implemented!")

    def move_forward(self, dist, direct):
        raise NotImplementedError("Not implemented!")

    def get_pos(self):
        """"""
        return (self.pos[0], self.pos[1])


class ShipPart2(Ship):
    """"""
    def __init__(self):
        """"""
        self.pos = np.array([0, 0])
        self.directions = np.array([Direction.RIGHT, Direction.UP])
        self.waypoint = np.array([10, 1])

    def turn_left(self, degree):
       a = np.dot(Direction.COORDS[self.directions[0]], self.waypoint)
       b = np.dot(Direction.COORDS[self.directions[1]], self.waypoint)

       self.directions = (self.directions - degree//90) % 4
       self.waypoint = a*Direction.COORDS[self.directions[0]] + b*Direction.COORDS[self.directions[1]]

    def turn_right(self, degree):
        a = np.dot(Direction.COORDS[self.directions[0]], self.waypoint)
        b = np.dot(Direction.COORDS[self.directions[1]], self.waypoint)

        self.directions = (self.directions + degree//90) % 4
        self.waypoint = a*Direction.COORDS[self.directions[0]] + b*Direction.COORDS[self.directions[1]]

    def move_forward(self, dist, direct):
        """"""
        if direct == Direction.FORWARD:
            self.pos = self.pos + dist * self.waypoint
        else:
            self.waypoint = self.waypoint + dist*Direction.COORDS[direct]


class ShipPart1(Ship):
    """"""
    def __init__(self):
        """"""
        self.pos = np.array([0, 0])
        self.direction = Direction.RIGHT

    def turn_left(self, degree):
        self.direction = (self.direction - degree//90) % 4

    def turn_right(self, degree):
        self.direction = (self.direction + degree//90) % 4

    def move_forward(self, dist, direct):
        """"""
        if direct == Direction.FORWARD:
            self.pos = self.pos + dist * Direction.COORDS[self.direction]
        else:
            self.pos = self.pos + dist * Direction.COORDS[direct]


def main():
    data = load_input()

    b = Board(data.copy(), ShipPart1())
    print("Part1: ", b.start())

    b = Board(data.copy(), ShipPart2())
    print("Part2: ", b.start())



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
