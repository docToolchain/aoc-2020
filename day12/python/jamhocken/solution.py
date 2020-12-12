import re

def process_input(file_contents):      
    container = list()
    regex_cmd = re.compile('(\S{1})(\d+)')
    for code_lines in file_contents:
        temp_line = regex_cmd.match(code_lines)
        container.append((temp_line.group(1),int(temp_line.group(2))))
    return container

def rotate_ship(dp_prev, value):
    cardinal_directions = ['N','E','S','W']
    turns = value // 90
    car_dir = cardinal_directions.index(dp_prev[0])
    return (cardinal_directions[(car_dir+turns) % 4],dp_prev[1],dp_prev[2])

def calculate_dp(dp_prev, value, code):
    if code == 'E':
        return (dp_prev[0],dp_prev[1],dp_prev[2] + value)
    elif code == 'W':
        return (dp_prev[0],dp_prev[1],dp_prev[2] - value)
    elif code == 'N':
        return (dp_prev[0],dp_prev[1]+value,dp_prev[2])
    elif code == 'S':
        return (dp_prev[0],dp_prev[1]-value,dp_prev[2])
    elif code == 'F':
        return calculate_dp(dp_prev,value,dp_prev[0])
    else:
        if code == 'L':
            value *= -1
        return rotate_ship(dp_prev, value)

def rotate_ship(dp_prev, value):
    cardinal_directions = ['N','E','S','W']
    turns = value // 90
    car_dir = cardinal_directions.index(dp_prev[0])
    return (cardinal_directions[(car_dir+turns) % 4],dp_prev[1],dp_prev[2])

def move_waypoint(wp_prev, value, code):
    if code == 'E':
        return (wp_prev[0],wp_prev[1] + value)
    elif code == 'W':
        return (wp_prev[0],wp_prev[1] - value)
    elif code == 'N':
        return (wp_prev[0]+value,wp_prev[1])
    elif code == 'S':
        return (wp_prev[0]-value,wp_prev[1])

def rotate_wp(wp_prev, value):
    turns = value // 90
    wp_temp = wp_prev
    for i in range(turns):
        wp_temp = (wp_temp[1]*-1,wp_temp[0])
    return wp_temp

def move_ship(pos_prev, waypoint, value):
    north = value*waypoint[0] + pos_prev[0]
    east = value*waypoint[1] + pos_prev[1]
    return (north,east)

with open("instructions.txt",'r') as code_file:
    all_code_file = code_file.readlines()

all_codes = process_input(all_code_file)

dir_pos = [('E',0,0)]

for i in range(len(all_codes)):
    code_temp = all_codes[i]
    dir_pos.append(calculate_dp(dir_pos[i], code_temp[1], code_temp[0]))

print('The Manhattan distance between starting point and end of sequence is',\
      abs(dir_pos[i+1][1]) + abs(dir_pos[i+1][2]))

pos_list = [(0,0)]
waypoint = [(1,10)]
for i in range(len(all_codes)):
    movewp = ['N','S','E','W']
    rotatewp = ['L','R']
    moveship = 'F'
    code_temp = all_codes[i]
    if code_temp[0] in moveship:
        pos_list.append(move_ship(pos_list[i],waypoint[i],code_temp[1]))
        waypoint.append(waypoint[i])
    elif code_temp[0] in movewp:
        waypoint.append(move_waypoint(waypoint[i], code_temp[1], code_temp[0]))
        pos_list.append(pos_list[i])
    else:
        value = code_temp[1]
        if code_temp[0] == 'L':
            value = 360 - code_temp[1]
        waypoint.append(rotate_wp(waypoint[i], value))
        pos_list.append(pos_list[i])

print('With the corrected understanding, the Manhattan distance is ',\
      abs(pos_list[i+1][0]) + abs(pos_list[i+1][1]))