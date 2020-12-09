import math

trackback = 5

def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [int(item.strip()) for item in local_list]
        return return_list

def check_code(code, codes_sublist):
    for line, num1 in enumerate(codes_sublist):
        diff = code - num1
        for num2 in codes_sublist[line+1:]:
            if (diff == num2): return True
    return False


def get_next_XMAS_error(codes_list):
    cursor = trackback
    while (cursor < len(codes_list)):
        code = codes_list[cursor]
        if (not check_code(code, codes_list[cursor-trackback:cursor])):
            return code
        cursor += 1
    return 0

def filter_codelist(codes_list, max):
    return_list = [item for item in codes_list if (item < max)]
    return return_list

def get_codebreaking_list(goal, codes_list, summands = set()):
    reduced_list = filter_codelist(codes_list, goal)
    if (reduced_list == []): return None
    print(reduced_list, summands)
    for line, num in enumerate(reduced_list):
        new_goal = goal - num
        if (new_goal < 0): 
                continue
        summands.add(num)
        if (new_goal == 0): 
                return summands
        new_summands = get_codebreaking_list(new_goal, reduced_list, summands)
        if (not new_summands):
            summands.discard(num)
        else:
            summands.update(new_summands)
    return summands

def main():
    daily_list = read_daily_input('input_test.txt')
    star1 = get_next_XMAS_error(daily_list)
    print(f"First XMAS code error at: {star1}")
    star2_list = get_codebreaking_list(star1, daily_list)
    print(star2_list)
    star2 = min(star2_list) + max(star2_list)
    print(f"Breaking pair's sum: {star2}")

if __name__ == "__main__":
    main()


