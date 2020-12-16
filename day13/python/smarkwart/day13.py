import sys
import re
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

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

def find_earliest_departure(start_time, buses, max_wait_time):
    """
    Returns: bus_id, time_of_departure
    """
    for time_of_departure in range (start_time, start_time + max_wait_time):
        for bus_id in buses:
            if time_of_departure % bus_id == 0:
                return bus_id, time_of_departure
    return -1, -1

def print_timetable(start_time, buses, lines_to_print):
    print("time", end='')
    for bus in buses:
        print(f"\t{bus}", end='')
    print("")
    for time in range (start_time, start_time + lines_to_print):
        print(time, end='')
        for bus in buses:
            if time % bus == 0:
                print(f"\tD", end='')
            else:
                print(f"\t.", end='')
        print("")

cls()

input_data = get_input_data_as_list(sys.argv[1])

earliest_timestamp = int(input_data[0])
bus_ids = input_data[1].split(',')

buses_in_service = [int(id) for id in bus_ids if id != 'x']
buses_in_service.sort()

print_timetable(earliest_timestamp, buses_in_service, max(buses_in_service))

bus_id, time_of_departure = find_earliest_departure(earliest_timestamp, buses_in_service, min(buses_in_service))

print(f"Bus {bus_id} will depart at {time_of_departure} which is {time_of_departure - earliest_timestamp} minutes from now on. Puzzle #1 solution is: {bus_id * (time_of_departure - earliest_timestamp)}")

