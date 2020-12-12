import math

def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [int(item.strip()) for item in local_list]
        return return_list

def get_device_joltage(adapter_list):
    ''' Returns device joltage (max + 3)
    '''
    return max(adapter_list)+3

def get_adapter_ladder_1x3_product(adapter_list):
    ''' Star1: Counts different differences and sums them individually.
        Returns 1-differences * 3-differences.
    '''
    ones = 0
    twos = 0
    threes = 0
    for cursor in range(1,len(adapter_list)):
        delta = adapter_list[cursor] - adapter_list[cursor-1]
        if (delta == 3): threes += 1
        if (delta == 2): twos += 1
        if (delta == 1): ones += 1
        cursor += 1
    print(ones, twos, threes, len(adapter_list))
    return ones*threes

def reduce_list(adapter_list, max_jolt):
    ''' Reduces list to elements <= max_jolt
    '''
    return [item for item in adapter_list if item <= max_jolt]

def get_all_ladders(adapter_list, count = 1):
    ''' Star2 - first try: Reduce list and recursively count the paths
        Runs too long with puzzle input, although tests complete successfully
    '''
    adapter = adapter_list.pop(0)
    reduced_list = reduce_list(adapter_list, adapter + 3)
    if (reduced_list==[]):
        return count
    elif (len(reduced_list) == 1):
        count = get_all_ladders(adapter_list, count)
        return count
    else:
        count += len(reduced_list) - 1 # add new branches only
        add = 0
        for line, num in enumerate(reduced_list):
            new_count = get_all_ladders(adapter_list[line:], count)
            add += new_count - count
        return count + add

def get_ladders_efficiently(adapter_list, count = 1):
    ''' Star2 - more efficient solution: 
        Search for segments where difference < 3. 
        At difference == 3 there is a bottleneck where all paths cross.
        Use function get_all_ladders only for segments and multiply results.
        Returns count in ms :)
    '''
    segments = list()
    segment = [adapter_list[0],]
    for cursor in range(1,len(adapter_list)):
        delta = adapter_list[cursor] - adapter_list[cursor-1]
        if (delta == 3): 
            segments.append(segment)
            segment = list()
        segment.append(adapter_list[cursor])
    for segm in segments:
        if (len(segm) > 1):
            count *= get_all_ladders(segm)
    return count

def main():
    daily_list = read_daily_input('input10.txt')
    full_daily_list = daily_list.copy()
    full_daily_list.sort()
    full_daily_list.insert(0, 0)
    full_daily_list.append(get_device_joltage(daily_list))
    star1 = get_adapter_ladder_1x3_product(full_daily_list)
    print(f"Adapter ladder 1x3 step product: {star1}")
    # star2 = get_all_ladders(full_daily_list)
    star2 = get_ladders_efficiently(full_daily_list)
    print(f"All joltage ladder combinations: {star2}")

if __name__ == "__main__":
    main()


