import sys
import math

def get_input_data_as_list(file_name):
    """ Reads in data from the given file and returns them as list
        with one entry per line and whitespaced trimmed """
    with open(file_name) as input_file:
        #data_list = map(str.strip,input_file.readlines())
        data_list = input_file.readlines()
    return data_list

def ride_the_toboggan(hill_map, right, down=1):
    """
    We ride the roboggan down one line, 'right' steps right, 'down' rows down
    and count how many tress we hit
    """
    position = 0
    treess_hit = 0
    for row in hill_map[::down]:
        if '#' == row[position % len(row.strip())]:
            treess_hit += 1
        position += right
    return treess_hit

ride_plans = [
    {'right' : 1, 'down' : 1},
    {'right' : 3, 'down' : 1},
    {'right' : 5, 'down' : 1},
    {'right' : 7, 'down' : 1},
    {'right' : 1, 'down' : 2},
]

hill_map = get_input_data_as_list(sys.argv[1])
hit_trees = []

for plan in ride_plans:
    hit_trees.append(ride_the_toboggan(hill_map, plan['right'], plan['down']))
    print(f"Ouch, by going right {plan['right']} and down {plan['down']} we have hit {hit_trees[-1]} trees")

print(f"The answer for star 2 is: {math.prod(hit_trees)}")