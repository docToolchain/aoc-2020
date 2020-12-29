import re
import math
import copy


def read_file_to_list(filename):
        """Read file to map"""
        lines = []
        
        file = open(filename, "r")
        for line in file:
            line = line.strip()
            lines.append(line)
        return lines


class Tiles:
    def __init__(self):
        self.tiles = dict()

    def flip(self,x,y):
        key = "{0}#{1}".format(x,y)
        tile = { "color" : "white" , "pos" : (x,y) }
        if key in self.tiles:
            tile = self.tiles[key]
        if tile["color"] == "white": 
            tile["color"] = "black"
        else:
            tile["color"] = "white"
        self.tiles[key] = tile
    def isBlack(self,x,y):
        key = "{0}#{1}".format(x,y)
        if key in self.tiles:
            return self.tiles[key]["color"] == "black"
        return False
    def getBlackTilePositions(self):
        bt = set()
        for val in self.tiles.values():
            if val["color"] == "black": 
                bt.add(val["pos"])
        return bt
    def countBlack(self):
        return len(self.getBlackTilePositions())

#
#  00| 10| 20|
#     \ / \ /
#    11| 21| 31
#     / \ / \
#  12| 22| 32|

def flip_tiles(tiles,commands):
    l = len(commands)
    ix = 0
    x,y = (0,0)
    while ix < l:
        d = commands[ix]
        if d == 'e': x,y = x + 1,y
        if d == 'w': x,y = x - 1,y
        if d == 'n': 
            ix += 1
            d2 = commands[ix]
            if d2 == 'e': x,y = x,y - 1
            if d2 == 'w': x,y = x - 1,y - 1
        if d == 's': 
                ix += 1
                d2 = commands[ix]
                if d2 == 'e': x,y = x + 1,y + 1
                if d2 == 'w': x,y = x,y + 1
        ix += 1
    tiles.flip(x,y)

def calculate_neighbours(x,y):
    n = []
    n.append((x+1,y))
    n.append((x-1,y))
    n.append((x,y - 1))
    n.append((x-1,y - 1))
    n.append((x + 1,y + 1))
    n.append((x,y + 1))
    return n

def daily_flip_tiles(tiles):
    black_tiles = tiles.getBlackTilePositions()
    white_tiles = set()
    toflip = set()
    for (x0,y0) in black_tiles:
        neigbourPositions = calculate_neighbours(x0,y0)
        bl = 0
        for x,y in neigbourPositions:
            if tiles.isBlack(x,y):
                bl += 1
            else:
                white_tiles.add((x,y))
        if bl == 0 or bl > 2:
            toflip.add((x0,y0))
    for (x0,y0) in white_tiles:
        neigbourPositions = calculate_neighbours(x0,y0)
        bl = 0
        for x,y in neigbourPositions:
            if tiles.isBlack(x,y):
                bl += 1
        if bl == 2:
            toflip.add((x0,y0))
    for (x0,y0) in toflip:
        tiles.flip(x0,y0)