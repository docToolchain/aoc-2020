
def all_slopes(board, rowlength, slopes, treechar = '#'):
    res = 1
    for x,y in slopes:
        res *= num_trees_slope(board, rowlength, treechar=treechar, stride_x=x, stride_y=y)
    return res

def num_trees_slope(board, rowlength, treechar = '#', stride_x=3, stride_y=1):
    pos_x = 0
    pos_y = 0
    num_trees = 0
    while pos_y < len(board):
        row = board[pos_y]
        if row[pos_x] == treechar:
            num_trees += 1
        pos_x = (pos_x + stride_x) % rowlength
        pos_y += stride_y
    return num_trees

def parse_line(line, gameboard):
    gameboard.append(line)
    return gameboard

def main():
    input_filename = 'input.txt'
    star_number = 2
    with open(input_filename, 'r') as input:
        board = []
        cnt = 0
        for line in input:
            cnt += 1
            board = parse_line(line, board)
    if star_number == 1:
        num_trees = num_trees_slope(board, len(line), treechar='#')
        print('# trees (slope (3,1)): {}'.format(num_trees))
    if star_number == 2:
        slopes = [(1,1), (3,1), (5,1), (7,1), (1,2)]
        num_trees = all_slopes(board, len(line), slopes, treechar='#')
        print('prod(# trees) (all slopes): {}'.format(num_trees))

if __name__ == "__main__":
    main()