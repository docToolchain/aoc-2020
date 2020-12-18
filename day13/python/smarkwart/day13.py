import sys

def get_input_data_as_list(file_name):
    """ 
    Reads in data from the given file and returns them as list
        with one entry per line and whitespaced trimmed 
    """
    with open(file_name) as input_file:
        data_list = input_file.readlines()
    return data_list

def parse_bus_note(input_data):
    earliest_timestamp = int(input_data[0])
    all_buses = input_data[1].split(',')

    buses_in_service = [int(id) for id in all_buses if id != 'x']
    patched_bus_list = [int(id) if id != 'x' else 1 for id in all_buses]

    buses_in_service.sort()
    return earliest_timestamp, buses_in_service, patched_bus_list

def find_earliest_departure(start_time, buses):
    """
    Returns: bus_id, time_of_departure
    """
    for time_of_departure in range (start_time, start_time + min(buses)):
        for bus_id in buses:
            if time_of_departure % bus_id == 0:
                return bus_id, time_of_departure
    return -1, -1

def print_timetable(start_time, buses):
    print("time", end='')
    for bus in buses:
        print(f"\t{bus}", end='')
    print("")
    for time in range (start_time, start_time + max(buses)):
        print(time, end='')
        for bus in buses:
            if time % bus == 0:
                print(f"\tD", end='')
            else:
                print(f"\t.", end='')
        print("")

def find_subsequent_time(buses):
    increment = buses[0]
    time = buses[0]
    for idx,bus_id in enumerate(buses):
        while ((time+idx) % bus_id) != 0 or ((time+idx+1) % buses[idx+1]) !=0:
            time += increment
        # next entry is already last bus
        if buses[idx+1] == buses[-1]:
            return time
        increment *= buses[idx+1]

input_data = get_input_data_as_list(sys.argv[1])

start_time, buses_in_service, all_buses = parse_bus_note(input_data)

#print_timetable(start_time, buses_in_service)

bus_id, time_of_departure = find_earliest_departure(start_time, buses_in_service)

print(f"Bus {bus_id} will depart at {time_of_departure} which is {time_of_departure - start_time} minutes from now on. Puzzle #1 solution is: {bus_id * (time_of_departure - start_time)}")

time_x = find_subsequent_time(all_buses)
print(f"Start time for subsequent bus departure: {time_x}")
