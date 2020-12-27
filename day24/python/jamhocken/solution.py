import re

def process_input(file_contents):
    direction = re.compile("(e|w|se|ne|nw|sw)")
    instructions = [direction.findall(line) for line in file_contents]

    return instructions

def location(instruction):
    northeast = 0
    east = 0
    for i in instruction:
        if i == "ne":
            northeast += 1
        elif i == "sw":
            northeast -= 1
        elif i == "nw":
            northeast += 1
            east -= 1
        elif i == "se":
            northeast -= 1
            east += 1
        elif i == "e":
            east += 1
        else:
            east -= 1

    return (east,northeast)

def automat(tiles_set,cycles):
    vectors = [[0,0],[1,0],[-1,0],[0,1],[0,-1],[-1,1],[1,-1]]
    for cycle in range(cycles):
        new_position_set = set()
        tiles_set_temp = tiles_set.copy()
        for tile in tiles_set:
            for vector in vectors:
                new_position = tuple([a + b for a, b in zip(list(tile), vector)])
                if new_position not in new_position_set:
                    new_position_set.add(new_position)
                    neighbors = find_neighbors(tiles_set, new_position)
                    if new_position in tiles_set:
                        if neighbors == 0 or neighbors > 2: tiles_set_temp.remove(new_position)
                    elif neighbors == 2: tiles_set_temp.add(new_position)
        tiles_set = tiles_set_temp
    return tiles_set

def find_neighbors(tiles_set,position):
    vectors = [[1,0],[-1,0],[0,1],[0,-1],[-1,1],[1,-1]]
    neighbors = 0

    for vector in vectors:
        new_position = tuple([a + b for a, b in zip(list(position), vector)])
        if new_position in tiles_set: neighbors += 1

    return neighbors

def main():
    with open("tiles.txt",'r') as code_file:
        all_code_file = code_file.readlines()

    instructions = process_input(all_code_file)

    tiles = [location(instruction) for instruction in instructions]
    tile_set = set(tiles)
    for tile in tile_set.copy():
        if tiles.count(tile) % 2 == 0: tile_set.remove(tile)
    print("There are initially", len(tile_set), "black tiles.")

    print("After 100 days, there are", len(automat(tile_set.copy(), 100)),"black tiles.")

main()