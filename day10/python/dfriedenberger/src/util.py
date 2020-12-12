
import re
import copy

def read_file_to_list(filename):
    """Read file to List"""
    list = []
    file = open(filename, "r")
    for line in file:
            list.append(int(line.strip()))
    file.close()
    return list

