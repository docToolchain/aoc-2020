import utils

utils.getVersion()

input = utils.read_file_to_list("input.txt")

#print(input)

size = len(input)

for i in range(0, size):
    for j in range(0, size):
        if i != j:
            sum = input[i] + input[j]
        else:
            sum = 0
        if sum == 2020:
            print("sum = {}, i = {}, j = {}, val1 = {}, val2 = {}, multiplication = {}".format(sum,i,j,input[i],input[j],input[i]*input[j]))


