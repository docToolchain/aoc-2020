import math

def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = local_list
        # return_list = [int(item) for item in local_list] ## no casting on day03
        return return_list

def check_treechecks(single_line, current_position):
    ''' Checks single line at given position
        for tree ('#') or pas ('.')'''
    return (single_line[current_position]=='#')

def run_course(terrain_list, right, down):
    ''' Runs along given terrain with given slope, i.e.
        <right> amount of positions right, <down> amount down.
        Prints out result and returns trees hit.'''
    position = 0
    tree_count = 0
    for line_nr, line in enumerate(terrain_list):
        if (line_nr % down != 0): continue
        if check_treechecks(line, position):
            tree_count += 1
        position = (position + right) % (len(line)-1)
    #print("Trees hit @R{}D{}: {}".format(right, down, tree_count))
    print(f"Trees hit @R{right}D{down}: {tree_count}")
    return tree_count

daily_list = read_daily_input('input03.txt')
courses = [[1,1], [3,1], [5,1], [7,1], [1,2]]
results = list()

for course in courses:
    results.append(run_course(daily_list, course[0], course[1]))

print(f"Puzzle result: {math.prod(results)}")



