import sys
import re
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Waypoint:
    def __init__(self, position_lat, position_long):
        # Latitudinal (+north -south) position
        self.position_lat = position_lat
        # Longitudinal (+east -west) position
        self.position_long = position_long

    def move(self, instruction):
        direction = instruction['direction']
        value = int(instruction['value'])
        if direction == 'N':
            self.position_lat += value
        elif direction == 'S':
            self.position_lat -= value
        elif direction == 'E':
            self.position_long += value
        elif direction == 'W':
            self.position_long -= value
        elif direction == 'L' or direction == 'R':
            self.turn(instruction)
        #print(f"Waypoint N/E Q: {self.position_lat, self.position_long, self.get_quadrant()}")

    def turn(self, instruction):
        direction = instruction['direction']
        value = int(instruction['value'])

        if direction == 'R':
            sign = -1
        else:
            sign = 1

        quadrant = (self.get_quadrant() + (sign * int(value/90))) % 4

        self.position_lat, self.position_long = abs(self.position_lat), abs(self.position_long)

        if int(value/90)%2 == 1:
            self.position_lat, self.position_long = self.position_long, self.position_lat

        if quadrant == 1:
            self.position_long *= -1
        elif quadrant == 2:
            self.position_long *= -1
            self.position_lat *= -1
        elif quadrant == 3:
            self.position_lat *= -1
        #print(f"Q now {quadrant}")

    def get_quadrant(self):
        quadrant = 0
        if self.position_lat >= 0 and self.position_long >= 0:
            quadrant = 0
        elif self.position_lat >= 0 and self.position_long < 0:
            quadrant = 1
        elif self.position_lat < 0 and self.position_long < 0:
            quadrant = 2
        elif self.position_lat < 0 and self.position_long >= 0:
            quadrant = 3
        return quadrant

    def get_position(self):
        return self.position_lat, self.position_long
 
class Ship_star1:

    def __init__(self, initial_direction):
        # Latitudinal (+north -south) position
        self.position_lat = 0
        # Longitudinal (+east -west) position
        self.position_long = 0
        self.directions = ['N', 'E', 'S', 'W']
        self.direction_index = self.directions.index(initial_direction)

    def sail(self, instruction):
        direction = instruction['direction']
        value = int(instruction['value'])
        if direction == 'N':
            self.position_lat += value
        elif direction == 'S':
            self.position_lat -= value
        elif direction == 'E':
            self.position_long += value
        elif direction == 'W':
            self.position_long -= value
        elif direction == 'L' or direction == 'R':
            self.turn(instruction)
        elif direction == 'F':
            new_instruction = {'direction' : self.directions[self.direction_index], 'value' : value}
            self.sail(new_instruction)
            pass

    def turn(self, instruction):
        directions = ['N', 'E', 'S', 'W']
        offset = int(int(instruction['value']) / 90)
        if instruction['direction'] == 'L':
            offset *= -1
        self.direction_index = (self.direction_index + offset) % len(directions)
        pass

    def get_position(self):
        return self.position_lat, self.position_long

class Ship_star2:

    def __init__(self, initial_direction):
        # Latitudinal (+north -south) position
        self.position_lat = 0
        # Longitudinal (+east -west) position
        self.position_long = 0
        self.directions = ['N', 'E', 'S', 'W']
        self.direction_index = self.directions.index(initial_direction)
        self.waypoint = Waypoint(1, 10)

    def sail(self, instruction):
        value = int(instruction['value'])
        if instruction['direction'] != 'F':
            self.waypoint.move(instruction)
        else:
            waypoint_lat, waypoint_long = self.waypoint.get_position()
            self.position_lat += value * waypoint_lat
            self.position_long += value * waypoint_long

    def get_position(self):
        return self.position_lat, self.position_long

def get_input_data_as_list(file_name):
    """ 
    Reads in data from the given file and returns them as list
        with one entry per line and whitespaced trimmed 
    """
    with open(file_name) as input_file:
        data_list = input_file.readlines()
    return data_list

def parse_instructions(instruction_list):
    """
    Parses the instruction strings into a dictionary
    """
    instruction_dict = []
    for instruction in instruction_list:
        regex_match = re.match(r"(?P<direction>\w)(?P<value>\d*)",instruction)
        if regex_match:
            instruction_dict.append(regex_match.groupdict())
    return instruction_dict

def lets_sail(ship, navigation_instructions):
    for instruction in navigation_instructions:
        #print(f"Nav: {instruction}")
        ship.sail(instruction)
        #print(f"Ship N/E: {ship.get_position()}")

def get_manhatten_distance(position):
    return abs(position[0]) + abs(position[1])

cls()

input_data = get_input_data_as_list(sys.argv[1])

ferry = Ship_star1('E')
lets_sail(ferry, parse_instructions(input_data))
print(f"The manhatten distance for star 1 is: {get_manhatten_distance(ferry.get_position())}")

ferry = Ship_star2('E')
lets_sail(ferry, parse_instructions(input_data))
print(f"The manhatten distance for star 2 is: {get_manhatten_distance(ferry.get_position())}")

