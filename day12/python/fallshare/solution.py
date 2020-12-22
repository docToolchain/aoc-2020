from pathlib import Path
import itertools
import copy

FLOOR = "."
EMPTY_SEAT = "L"
TAKEN = "#"

def read_input_file(input_file_path):
    p = Path(input_file_path)

    commands = list(dict())

    with p.open() as f:
        raw_commands = f.read().split("\n")
        for raw_command in raw_commands:

            command = dict()
            command["instruction"] = raw_command[0]
            command["value"] = int(raw_command[1:])
            commands.append(command)

    return commands

def move_ship_star2(commands):
    x_wp = 10
    y_wp = 1
    x = 0
    y = 0
   

    for command in commands:
        #print(f"{command['instruction'] }{command['value']} Ship: {x},{y} - Wp: {x_wp}, {y_wp}")
        #move the waypoint
        if command["instruction"]== "N":
            y_wp += command["value"]
        elif command["instruction"] == "S":
            y_wp -= command["value"]
        elif command["instruction"] == "E":
            x_wp += command["value"]
        elif command["instruction"] == "W":
            x_wp -= command["value"]
        #rotate the waypoint
        elif command["instruction"] == "L":
            times = int(command["value"]/90)
            for i in range(times):  
                dx = x_wp
                dy = y_wp
                x_wp = -dy
                y_wp = +dx
            
        elif command["instruction"] == "R":
            times = int(command["value"]/90)
            for i in range(times):  
                dx = x_wp
                dy = y_wp
                x_wp = +dy
                y_wp = -dx
            
        elif command["instruction"] == "F":          
            x = x + x_wp * command["value"]
            y = y + y_wp * command["value"]          
        else:
            print("This should never happen")

    return x, y


if __name__ == "__main__":

    commands = read_input_file("input.txt")
    #x, y = move_ship_star1(commands)
    #print(f"Solution Star 1: Location of ship is ({x}|{y}) - manhattan distance: {abs(x) + abs(y)}" )
    x, y = move_ship_star2(commands)
    print(f"Solution Star 2: Location of ship is ({x}|{y}) - manhattan distance: {abs(x) + abs(y)}" )