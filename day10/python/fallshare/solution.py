from pathlib import Path
import itertools


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        data = list(map(int, f.readlines()))
    data.sort()
    return data

def add_device(data):
    data.append(max(data) + 3)
    return data

def get_histogram(data):
    histogram = [0, 0, 0]

    for i in range(1, len(data)): 
        diff = data[i] - data[i - 1] - 1
        histogram[diff] += 1

    return histogram



def breakdown_data(data):
    # all adapters in the box where the next adapter has a jolt distance of 3 
    # must be in the adapter chain otherwhise no chain can be formed
    # thoes adapters can be seen as seperators that can be used to split down the big bag of adapters
    # into smaller list of adapters
    # the possible combinations for those smaller list can  individually be calculated
    # in the end the amout of combinations of the sublist is multiplied to get the  total number of possible combinations
    

    adapters_with_max_distance = list()
    total_combinations = 1

    # find all adapters that act as seperators
    for i in range(1, len(data)):
        diff = data[i] - data[i - 1]         
        if diff == 3:
            adapters_with_max_distance.append(i - 1)
    
    # split down list of adapters into sub list and calculate posible combinations per list
    lower_bound = 0
    for j in range(1, len(adapters_with_max_distance)):
        upper_bound = adapters_with_max_distance[j]

        sub_list = data[lower_bound : upper_bound + 1]
        lower_bound = upper_bound + 1
        
        global combinations
        combinations = 0
        #use a recursive function to collect all possible combinations in the sub list
        recurse_through_data(sub_list,0,0)

        total_combinations *= combinations
    
    return total_combinations



def recurse_through_data(data,index,depth):
    global combinations

    if len(data) == 1:
        combinations = 1
        return    
    
    for i in range(1,4):
        #abort if last element is found
        diff = data[index + i] - data[index]

        if (data[index + i] == max(data)) and (diff <= 3):
            #print(f"i:{i} index: {index} depth:{depth} {max(data)}")
            combinations += 1
            return 

        #abort if end is found
        if (index + i) >= len(data):
            return 
        
        if diff <= 3:
            #print(f"{data[index + i]}", end = " ")
            recurse_through_data(data, index + i, depth + 1)
        else:
            #abort since next elemnt is not matching         
            return 

    return



   
if __name__ == "__main__":

    adapters = read_input_file("input.txt")
    adapters = add_device(adapters)
    #add source
    adapters.insert(0,0)
    histogram = get_histogram(adapters)
    
    print(f"Star 1: Solution {histogram[0] * histogram[2]}")


    adapter = read_input_file("input.txt")
    adapter = add_device(adapter)
    #add source
    adapter.insert(0,0)
 
    print(f"Star 2: Solution {breakdown_data(adapter)}")
    
