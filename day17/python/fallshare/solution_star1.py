from pathlib import Path
import itertools
import copy
import re



def read_input_file(input_file_path, input_cycles):
    #making the map bigger so that we dont get out of bound errors
    cycles = input_cycles + 1 
    p = Path(input_file_path)

    start_data = list(list())

    with p.open() as f:
        raw_rows = f.read().split("\n")
        y_width = len(raw_rows) + 2 * cycles
        x_width = len(raw_rows[0]) + 2 * cycles

        #construct initial map
        column = ['.'] * y_width
        for i in range(0, x_width):
            start_data.append(copy.deepcopy(column)) 

        full_map = list()
        for z in range(-cycles, cycles +1):
            full_map.append(copy.deepcopy(start_data))
        
        #read in stat state from file        
        for y in range(0, len(raw_rows)):
            for x in range(0, len(raw_rows[y])):
                full_map[cycles][x + cycles][y + cycles ] = raw_rows[x][y]     

        #print_map(full_map)
    return full_map

def print_map(full_map):
    for level in full_map:
        print_level(level)
        print()

def print_level(data):
    for column in data:
        print(column)

def process_map(start_map, cycles):
    current_map = start_map
    for i in range(0, cycles):
        new_map = copy.deepcopy(current_map)
        #iterate through all elements of map
        for z in range(1,len(current_map) - 1):
            for y in range(1,len(current_map[0]) - 1):
                for x in range(1,len(current_map[0][0]) - 1):
                    neighbours = get_neighbours(current_map,z,y,x)
                    if neighbours == 3:
                       new_map[z][y][x] = "#"
                    elif neighbours == 2 and current_map[z][y][x] == "#":
                       new_map[z][y][x] = "#"
                    else:
                       new_map[z][y][x] = "."
        current_map = copy.deepcopy(new_map)
        #print_map(current_map)
    return current_map

def get_neighbours(new_map,z,y,x):
    neighbours = 0
    for dz in [-1, 0 ,1]:
        for dy in [-1, 0 ,1]:
            for dx in [-1, 0 ,1]:
                if not (dz == 0 and dy == 0 and dx == 0):
                    if new_map[z+dz][y+dy][x+dx] == "#":
                        neighbours += 1
    return neighbours

def get_active_coordinates(current_map):
    active_cooridnates = 0
    for z in range(0,len(current_map)):
        for y in range(0,len(current_map[0])):
            for x in range(0,len(current_map[0][0])):
                 if current_map[z][y][x] == "#":
                     active_cooridnates += 1
    return active_cooridnates

if __name__ == "__main__":

    cycles = 6
    start_map = read_input_file("input.txt", cycles)
    final_map = process_map(start_map, cycles)
    print(f"Star 1: number of active coordinates is {get_active_coordinates(final_map)}")


    
   