import math

def process_input(file_contents):  
    temp = dict()
    for i,line in enumerate(file_contents):
        for j, seat in enumerate(line):
            if seat != '\n':
                temp.update({(i,j) : seat})
    return temp

# Helper function to visualize room in the command line
def visualize_room(data,max_column):
    for (i,j) in data:
        if j == max_column:
            print(data[i,j])
        else: print(data[i,j],end='')
    print('')
        
def automat(dictionary,problem):
    keys = max(dictionary.keys())
    max_row = keys[0]
    max_column = keys[1]
    flag = 1
    dict_temp = dictionary.copy()
    while flag == 1:
        flag = 0
        dictionary = dict_temp.copy()
        for key, value in dictionary.items():
            if value != '.':
                neighbors = find_neighbors(dictionary,key,problem,max_row,max_column)
                if value == 'L' and sum(neighbors) == 0:
                    dict_temp.update({key : '#'})
                    flag = 1
                if value == '#' and ((sum(neighbors) > 3 and problem == 1) \
                                     or (sum(neighbors) > 4)):
                    dict_temp.update({key:'L'})
                    flag = 1

    return dict_temp

def find_neighbors(dictionary,key,problem,max_row,max_column):
    vectors = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,0],[0,1],[1,-1],[1,0],[1,1]]
    neighbors = list()
    
    for vector in vectors:
        new_key = tuple([a + b for a, b in zip(list(key), vector)])
        if problem == 1:
            if new_key[0] > max_row or new_key[0] < 0 or \
                new_key[1] > max_column or new_key[1] < 0 or vector == [0,0]:
                neighbors.append(0)
            else:
                if dictionary[new_key] == '#': neighbors.append(1)
                else: neighbors.append(0)
        elif problem == 2:
            flag = 0
            while flag == 0:    
                if new_key[0] > max_row or new_key[0] < 0 or \
                new_key[1] > max_column or new_key[1] < 0 or vector == [0,0]:
                    neighbors.append(0)
                    flag = 1
                else:
                    if dictionary[new_key] == '#':
                        neighbors.append(1)
                        flag = 1
                    elif dictionary[new_key] == 'L':
                        neighbors.append(0)
                        flag = 1
                    else:
                        new_key = tuple([a + b for a, b in zip(list(new_key), vector)])

    return neighbors

with open("life.txt",'r') as seat_file: 
    all_seat_file = seat_file.readlines()

seats = process_input(all_seat_file)
           
seat_temp = automat(seats.copy(),1)

print('For problem 1,', list(seat_temp.values()).count('#'),\
      'seats are occupied')

seat_temp = automat(seats.copy(),2)

print('For problem 2,', list(seat_temp.values()).count('#'),\
      'seats are occupied')