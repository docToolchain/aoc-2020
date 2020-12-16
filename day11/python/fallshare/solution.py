from pathlib import Path
import itertools
import copy

FLOOR = "."
EMPTY_SEAT = "L"
TAKEN = "#"

def read_input_file(input_file_path):
    p = Path(input_file_path)

    map = list(list())

    with p.open() as f:
        raw_rows = f.read().split("\n")
        for row in raw_rows:
            #normalize entry by removing new lines
            map.append(list(row))

    return map

def print_map(map):
    for row in map:
        for column in row:
            print(column, end = "")
        print("")
    print("")

def process_until_stable_star1(new_map):
    #first iteration
    old_map = copy.deepcopy(new_map)
    #print_map(old_map)

    new_map = process_star1(new_map)  
    #print_map(new_map)

    while(not are_identical(old_map, new_map)):
        old_map = copy.deepcopy(new_map)
 
        new_map = process_star1(new_map) 

       # print_map(new_map)     

    return new_map

def are_identical(old_map, new_map):
    for i in range (0, len(new_map)):
        #print(f"{old_map[i]} - {new_map[i]}")
        if old_map[i] != new_map[i]:
            #print("stop")
            return False
    
    return True

def process_star1(map):
 
    new_map = copy.deepcopy(map)

    for y in range(0, len(map)):
        for x in range(0, len(map[y])):
            #print(f"x:{x} y:{y}")
            new_map[y][x] = calculate_new_state_star1(map, y ,x)
            #print("")

    return new_map    

def get_occupied_neighbours_star1(map, x ,y):
    occupied_seats = 0

    for dy in [-1, 0, 1]:
            if (0 <= (dy + y) < len(map)):
                for dx in [-1, 0, 1]:
                    #check that we dont exceed boundaries
                    
                    if (0 <= (dx + x) < len(map[y])) and not ((dx == 0) and (dy == 0)):
                        #print(f"dx {dx} : dy {dy} : {map[y + dy][dx + x]}")
                        if map[y + dy][dx + x] == TAKEN:
                            occupied_seats += 1
    #print(f"occupied seats: {occupied_seats}")
    return occupied_seats

def calculate_new_state_star1(map, y ,x):

    if map[y][x] == FLOOR:
        return FLOOR

    if map[y][x] == EMPTY_SEAT:            
        if get_occupied_neighbours_star1(map, x ,y) == 0:
            return TAKEN
        else:
            return EMPTY_SEAT

    if map[y][x] == TAKEN:
        # print(get_occupied_neighbours(map, x ,y))

        if get_occupied_neighbours_star1(map, x ,y) >= 4:
            return EMPTY_SEAT
        else:
            return TAKEN
    #umfeld abfahren und zustaende zaehlen
    return EMPTY_SEAT

def process_until_stable_star2(new_map):
    #first iteration
    old_map = copy.deepcopy(new_map)
    #print_map(old_map)

    new_map = process_star2(new_map)  
    #print_map(new_map)

    while(not are_identical(old_map, new_map)):
        old_map = copy.deepcopy(new_map)
 
        new_map = process_star2(new_map) 

        #print_map(new_map)     

    return new_map

def process_star2(map):
 
    new_map = copy.deepcopy(map)

    for y in range(0, len(map)):
        for x in range(0, len(map[y])):
            #print(f"x:{x} y:{y}")
            new_map[y][x] = calculate_new_state_star2(map, y ,x)
            #print("")

    return new_map    

def calculate_new_state_star2(map, y ,x):

    if map[y][x] == FLOOR:
        return FLOOR

    if map[y][x] == EMPTY_SEAT:            
        if get_occupied_neighbours_star2(map, x ,y) == 0:
            return TAKEN
        else:
            return EMPTY_SEAT

    if map[y][x] == TAKEN:
        # print(get_occupied_neighbours(map, x ,y))

        if get_occupied_neighbours_star2(map, x ,y) >= 5:
            return EMPTY_SEAT
        else:
            return TAKEN
  
    return EMPTY_SEAT

def get_occupied_neighbours_star2(map, x ,y):
    occupied_seats = 0

    for dy in [-1, 0, 1]:
            if (0 <= (dy + y) < len(map)):
                for dx in [-1, 0, 1]:
                    #check that we dont exceed boundaries
                    
                    if (0 <= (dx + x) < len(map[y])) and not ((dx == 0) and (dy == 0)):
                        #print(f"dx {dx} : dy {dy} : {map[y + dy][dx + x]}")
                        #scan every of the eight directions around the seat
                        occupied_seats += scan(map, x, y, dx, dy)
    #print(f"x:{x} y:{y} occu: {occupied_seats}")
    return occupied_seats    

def scanner_in_map(map,scanner_x,scanner_y):
    #check if scanner beam is still within the map
    if 0 <= scanner_x and 0 <= scanner_y and scanner_x < len(map[0]) and scanner_y < len(map):
        return True
    else:
        return False

def scan(map, x, y, dx, dy):
    #shots a scan beam across the beam until a occupied seatis found or the end the map is reached
    scanner_y = y + dy
    scanner_x = x + dx

    while(scanner_in_map(map,scanner_x,scanner_y)):
        if map[scanner_y][scanner_x] == TAKEN:
            return 1
        if map[scanner_y][scanner_x] == EMPTY_SEAT:
            return 0
        scanner_x += dx
        scanner_y += dy

    return 0

def count_occupied_seats(map):
    occupied_seats = 0
    for row in map:
        for seat in row:
            if seat == TAKEN:                
                occupied_seats += 1
    
    return occupied_seats


if __name__ == "__main__":

    map = read_input_file("input.txt")
    map = process_until_stable_star1(map)
    print(f"Star 1: {count_occupied_seats(map)} seats are taken")

    map = read_input_file("input.txt")
    map = process_until_stable_star2(map)
    print(f"Star 2: {count_occupied_seats(map)} seats are taken")