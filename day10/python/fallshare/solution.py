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
    histogram = [1, 0, 0]

    for i in range(1, len(data)):
        diff = data[i] - data[i - 1] - 1
        histogram[diff] += 1

    return histogram

def get_possible_combinatios(data):
   
    recurse_through_data(data, 0, 0)

    return



def recurse_through_data(data,index,depth):
    global combinations
    for i in range(1,4):
        #abort if last element is found
        print(f"depth:{depth} - i: {i}")
        if data[index + i] == max(data):
            print(f"i:{i} index: {index} depth:{depth} {max(data)}")
            combinations += 1
            return 
        #abort if end is found
        if (index + i) >= len(data):
            return 

        diff = data[index + i] - data[index]
        if diff <= 3:
            print(f"{data[index + i]}", end = " ")
            recurse_through_data(data, index + i, depth + 1)
        else:
            #abort since next elemnt is not matching         
            return 

    return



   
if __name__ == "__main__":

    adapters = read_input_file("input.txt")
    adapters = add_device(adapters)
    histogram = get_histogram(adapters)
    
    print(f"Star 1: Solution {histogram[0] * histogram[2]}")


    adapter_2 = read_input_file("input.txt")
    adapter_2 = add_device(adapter_2)
    #add source
    adapter_2.insert(0,0)
    global combinations 
    combinations = 0
    get_possible_combinatios(adapter_2)
    print(combinations)

