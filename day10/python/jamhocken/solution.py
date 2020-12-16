import math

def process_input(file_contents):  
    return [int(line) for line in file_contents]

def find_combinations(width):
    if width <= 1:
        return 1
    elif width == 2:
        return 2
    elif width == 3:
        return 4
    else:
        return 2*find_combinations(width-1) - find_combinations(width-4)
#       return find_combinations(width-1) + find_combinations(width-2) + find_combinations(width-3)

with open("adapters.txt",'r') as adapters_file:
    all_adapters_file = adapters_file.readlines()

adapters = process_input(all_adapters_file)
adapters.append(0)
adapters.append(max(adapters)+3)
adapters.sort()

diff = [adapters[i+1]-adapters[i] for i in range(len(adapters)-1)]    

print('The number of 1 jolt difference is', diff.count(1))
print('The number of 3 jolt difference is', diff.count(3))
print('Their product is', diff.count(1)*diff.count(3))

depth = 0
count = list()
while depth < len(diff):
    depth2 = diff.index(3,depth)
    if depth2-depth < 2:
        count.append(1)
        depth = depth2 + 1
    else:
        diff_temp = diff[depth:depth2]
        count.append(find_combinations(len(diff_temp)))
        depth = depth2 + 1
        
print('The total number of distinct ways to arrange the adapters to connect\
  the charging outlet to my device is', math.prod(count))   

def alt_find_combinations(list_adapters):
    adapter_dictionary = {0 : 1}

    for adapter in list_adapters[1:len(list_adapters)]:
        sums = 0
        for i in range(1, 4):
            next_adapter = adapter - i
            if next_adapter in list_adapters:
                sums += adapter_dictionary[next_adapter]
        adapter_dictionary[adapter] = sums
    print(adapter_dictionary)
    return adapter_dictionary[max(list_adapters)]

print('The total number of distinct ways to arrange the adapters to connect\
  the charging outlet to my device is', alt_find_combinations(adapters))