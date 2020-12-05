
import math

def read_file_to_list(filename):
    """Read file to List"""
    list = []
    file = open(filename, "r")
    for line in file:
        list.append(line.strip())
    file.close()
    return list


def get_int(seat):
    
    row = 0
    col = 0
 
    for i in range(7):
        ix = 6 - i
        if(seat[ix] == 'B'):
            row += math.pow(2,i) 
    
    for i in range(3):
        ix = 9 - i 
        if(seat[ix] == 'R'):
            col += math.pow(2,i) 
    return row * 8 + col

