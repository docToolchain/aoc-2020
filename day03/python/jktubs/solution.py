import utils

utils.getVersion()

input = utils.read_file_to_list("input.txt")

# print(input)

size = len(input)
print("len: {}".format(size))
y_max = size

line_len = 0
for l in input:
    if len(l) > line_len:
        line_len = len(l)
        print("length of line: {}".format(line_len))

x_max = line_len

result = utils.count_trees(input, x_max, y_max, 3, 1) # solution part 1 => 187!

# part 2
result = utils.count_trees(input, x_max, y_max, 1, 1)
result *= utils.count_trees(input, x_max, y_max, 3, 1)
result *= utils.count_trees(input, x_max, y_max, 5, 1)
result *= utils.count_trees(input, x_max, y_max, 7, 1)
result *= utils.count_trees(input, x_max, y_max, 1, 2)

print("result part2: {}".format(result)) # solution part 2 => 4723283400!
#trees (right: 3, down: 1): 187
#trees (right: 1, down: 1): 86
#trees (right: 3, down: 1): 187
#trees (right: 5, down: 1): 75
#trees (right: 7, down: 1): 89
#trees (right: 1, down: 2): 44
