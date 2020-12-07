def getVersion():
    print("AoC2020_Day3!")


def read_file_to_list(filename):
    list = []
    file = open(filename, "r")
    for line in file:
        list.append(line.strip())
    file.close()
    return list


def count_trees(input, x_max, y_max, right, down):
    delta_x = right
    delta_y = down
    trees = 0
    x_to_check = 0
    for y in range(down, y_max, down):
        #print("line: {}".format(y))
        # for x in range(0, x_max):
        #    print("char: {}".format(input[y][x]))
        x_to_check += delta_x
        #print("x_to_check: {}".format(x_to_check))
        if x_to_check > x_max - 1:
            x_to_check -= x_max
        #print("x_to_check: {}".format(x_to_check))
        #print("char to check: {}".format(input[y][x_to_check]))
        if "#" == input[y][x_to_check]:
            trees += 1

    print("trees (right: {}, down: {}): {}".format(right, down, trees))

    return trees
