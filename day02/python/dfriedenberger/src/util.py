


def read_file_to_list(filename):
    """Read file to List"""
    list = []
    file = open(filename, "r")
    for line in file:
        policy , password = line.split(':')
        range, character = policy.split(' ')
        fromRange, toRange = range.split('-') 
        list.append(( int(fromRange), int(toRange), character, password.strip()))
    file.close()
    return list

def count(password,character):
    count = 0
    for c in password:
       if(c == character):
           count = count + 1
    return count

def check(password,index,character):
    if(password[index-1] == character):
        return 1
    return 0
