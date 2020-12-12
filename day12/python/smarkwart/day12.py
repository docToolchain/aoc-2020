import sys
import re
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Ship:

    def __init__(self, position_lat, position_long, direction):
        # Latitudinal (+north -south) position
        self.position_lat = position_lat
        # Longitudinal (+east -west) position
        self.position_long = position_long
        self.directions = ['N', 'E', 'S', 'W']
        self.direction_index = self.directions.index(direction)

    def sail(self, instruction):
        #print(instruction)
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
        """
        docstring
        """
        directions = ['N', 'E', 'S', 'W']
        offset = int(int(instruction['value']) / 90)
        if instruction['direction'] == 'L':
            offset *= -1
        self.direction_index = (self.direction_index + offset) % len(directions)
        pass

    def get_position(self):
        #print(self.directions[self.direction_index])
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
        ship.sail(instruction)
        print(ship.get_position())

def get_manhatten_distance(position):
    return abs(position[0]) + abs(position[1])

cls()

input_data = get_input_data_as_list(sys.argv[1])

ferry = Ship(0,0,'E')

lets_sail(ferry, parse_instructions(input_data))

print(f"The manhatten distance for star 1 is: {get_manhatten_distance(ferry.get_position())}")

#directions = ['N', 'E', 'S', 'W']
#
#for x in range(-10,10):
#    print(directions[x%len(directions)])
