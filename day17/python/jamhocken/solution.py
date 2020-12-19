
def process_input(file_contents):
    temp = dict()
    for i, line in enumerate(file_contents):
        for j, seat in enumerate(line):
            if seat != '\n':
                temp.update({(0,0,i,j) : seat})

    return temp, len(file_contents)

# Helper function to visualize room in the command line
def visualize_room(data,max_column,round_no):
    temp_list = sorted(data)
    for (z,w,x,y) in temp_list:
        if y == max_column:
            print(data[z,w,x,y])
            if (x == max_column):
                print('z=', z, 'w=', w,'\n')
        else: print(data[z,w,x,y],end='')
    print('')

def automat(dictionary,cycles,problem):
    keys = max(dictionary.keys())
    max_z = keys[0]
    max_row = keys[2]
    min_row = 0
    max_column = keys[3]
    min_column = 0
    for cycle in range(cycles):
        for z in range(-1*max_z,max_z+1):
            for w in range(-1*max_z,max_z+1):
                for x in range(min_row-1,max_row+2):
                    dictionary.update({(z,w,x,min_column-1) : '.'})
                    dictionary.update({(z,w,x,max_column+1) : '.'})
                for y in range(min_column-1,max_column+2):
                    dictionary.update({(z,w,min_row-1,y) : '.'})
                    dictionary.update({(z,w,max_row+1,y) : '.'})
        for z in [-1*max_z-1, max_z+1]:
            for x in range(min_row-1,max_row+2):
                for y in range(min_column-1,max_column+2):
                    for w in range(-1*max_z-1,max_z+2):
                        dictionary.update({(z,w,x,y) : '.'})
        for w in [-1*max_z-1, max_z+1]:
            for x in range(min_row-1,max_row+2):
                for y in range(min_column-1,max_column+2):
                    for z in range(-1*max_z-1,max_z+2):
                        dictionary.update({(z,w,x,y) : '.'})
        max_z += 1
        max_row += 1
        min_row -= 1
        max_column += 1
        min_column -= 1
        dict_temp = dictionary.copy()
        for key, value in dictionary.items():
            if problem == 1: max_w = 0
            else: max_w = max_z
            neighbors = find_neighbors(dictionary,key,max_row,max_column,min_row,min_column,max_z,max_w)
            if sum(neighbors) == 3:
                dict_temp.update({key : '#'})
            elif value == '#' and sum(neighbors) == 2:
                dict_temp.update({key:'#'})
            else: dict_temp.update({key:'.'})
        dictionary = dict_temp.copy()
    return dictionary

def find_neighbors(dictionary,key,max_row,max_column,min_row,min_column,max_z,max_w):
    vectors = list()
    for i in range(-1,2):
        for j in range(-1,2):
            for k in range(-1,2):
                for l in range(-1,2):
                    vectors.append([i,j,k,l])
    neighbors = list()

    for vector in vectors:
        new_key = tuple([a + b for a, b in zip(list(key), vector)])
        if new_key[2] > max_row or new_key[2] < min_row or \
            new_key[3] > max_column or new_key[3] < min_column or \
                vector == [0,0,0,0] or \
                    new_key[0] < -1*max_z or new_key[0]>max_z or \
                        new_key[1] < -1*max_w or new_key[1]>max_w:
            neighbors.append(0)
        else:
            if dictionary[new_key] == '#': neighbors.append(1)
            else: neighbors.append(0)
    return neighbors

with open("input.txt",'r') as code_file:
    all_code_file = code_file.readlines()

initial_dimension, initial_size = process_input(all_code_file)

final_space1 = automat(initial_dimension.copy(), 6, 1)

count1 = 0
for key,value in final_space1.items():
    if value == '#' and key[1]==0: count1 += 1
print(count1,'cubes are left in the active state after the sixth cycle in 3D problem.')


final_space2 = automat(initial_dimension.copy(), 6, 2)

count2 = 0
for key,value in final_space2.items():
    if value == '#': count2 += 1

print(count2,'cubes are left in the active state after the sixth cycle in 4D problem.')




