from pathlib import Path
import itertools
import math


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        data = f.readlines()
    
    arrival = int(data[0])
    bus_lines = data[1].split(",")
  
    return arrival, bus_lines

def find_next_leaving_bus(arrival, bus_lines):
    bus_lines = list(filter(("x").__ne__, bus_lines))
    bus_lines = [int(i) for i in bus_lines]

    #calculate next bus leave time per line
    next_leave_times = list()
    for line in bus_lines:
        next_leave_time = math.ceil((arrival / line)) * line
        next_leave_times.append(next_leave_time)

    closest_wait_time = 1000
    closest_line = 0
    for time in next_leave_times:
        wait_time = time - arrival
        if wait_time < closest_wait_time:
            closest_wait_time = wait_time
            closest_line = bus_lines[next_leave_times.index(time)]
    #check which line leaves next
    return closest_line, closest_wait_time


def find_star2_solution(bus_lines):
    real_bus_lines = list(filter(("x").__ne__, bus_lines))
    real_bus_lines = [int(i) for i in real_bus_lines]

    ref_time = int(real_bus_lines[0])
    time = 0

    for bus in real_bus_lines:
        flag = 1
        i = 0
        index = bus_lines.index(str(bus))

        while (time + ref_time * i + index) % bus != 0:
            i += 1

        time = time + ref_time * i
        if index != 0:
            ref_time = ref_time * bus
    return time


if __name__ == "__main__":

    arrival, bus_lines = read_input_file("input.txt")
    closest_line, closest_wait_time = find_next_leaving_bus(arrival, bus_lines)
    print(f"Star 1: Closest line is: {closest_line}, wait time: {closest_wait_time} - solution {closest_line * closest_wait_time}")
    print(f"Star 2: Next timestamp: {find_star2_solution(bus_lines)}")

