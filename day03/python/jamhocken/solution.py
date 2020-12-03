def collision(horizontal, vertical, width, row, pattern):
    if row % vertical == 0:
        if pattern[((horizontal*row) // vertical) % width] == '#':
            return True
        else:
            return False

crashes_0 = 0
crashes_1 = 0
crashes_2 = 0
crashes_3 = 0
crashes_4 = 0

count = 0

with open("trees.txt",'r') as map_file: 
    throwaway_first_line = map_file.readline()

    for line in map_file:
        line_stripped = line.rstrip()
        width = len(line_stripped)
        count += 1
        
        if collision(1,1,width,count,line_stripped): crashes_0 += 1
        if collision(3,1,width,count,line_stripped): crashes_1 += 1
        if collision(5,1,width,count,line_stripped): crashes_2 += 1
        if collision(7,1,width,count,line_stripped): crashes_3 += 1
        if collision(1,2,width,count,line_stripped): crashes_4 += 1

print('With the pattern Right 1, Down 1, there were', crashes_0, 'trees.')
print('With the pattern Right 3, Down 1, there were', crashes_1, 'trees.')
print('With the pattern Right 5, Down 1, there were', crashes_2, 'trees.')
print('With the pattern Right 7, Down 1, there were', crashes_3, 'trees.')
print('With the pattern Right 1, Down 2, there were', crashes_4, 'trees.')
print('The product is:', crashes_0*crashes_1*crashes_2*crashes_3*crashes_4)
