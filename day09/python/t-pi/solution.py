import math

trackback = 25

def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [int(item.strip()) for item in local_list]
        return return_list

def check_code(code, codes_sublist):
    ''' Boolean check if any two number in sublist sum up to code
    '''
    for line, num1 in enumerate(codes_sublist):
        diff = code - num1
        for num2 in codes_sublist[line+1:]:
            if (diff == num2): return True
    return False


def get_next_XMAS_error(codes_list):
    ''' Runs through codes_list with sliding window to check XMAS consistence
    '''
    cursor = trackback
    while (cursor < len(codes_list)):
        code = codes_list[cursor]
        if (not check_code(code, codes_list[cursor-trackback:cursor])):
            return code
        cursor += 1
    return 0

def reduce_codelist(codes_list, max):
    ''' Removes any values > max from codes_list
    '''
    return_list = [item for item in codes_list if (item <= max)]
    return return_list

def get_non_contigous_codebreaking_list(goal, codelist, summands = list()):
    ''' AMBIGUOUS RESULTS! Needed to look up contiguous...
        Recursively tests for any summands in codes_list, whether they sum up to goal
        Returns set of summands
    '''
    reduced_list = reduce_codelist(codelist, goal)
    if (reduced_list == []): 
        summands.pop()
        return summands
    for line, num in enumerate(reduced_list):
        new_goal = goal - num
        if (new_goal < 0): 
            continue
        summands.append(num)
        if (new_goal == 0): 
            return summands
        summe = sum(summands)
        summands = get_non_contigous_codebreaking_list(new_goal, reduced_list[line + 1:], summands)
        if ((sum(summands)-summe) == new_goal): return summands
        if (line == len(reduced_list)-1): summands.pop()
    return summands

def get_contiguous_codebreaking_list(goal, codes_list):
    ''' Runs through reduced list with sliding window to find contiguous numbers summing up to goal.
        Window is increased until either sum is found or sum > goal
        Returns sum's window.
    '''
    reduced_list = reduce_codelist(codes_list, goal)
    for line, num in enumerate(reduced_list):
        sum = 0
        cursor = line
        while ((sum < goal) and (cursor < len(reduced_list))):
            sum += reduced_list[cursor]
            cursor += 1
            if (sum == goal):
                return reduced_list[line:cursor]
            if (sum > goal):
                break
    return []
        
def main():
    daily_list = read_daily_input('input09.txt')
    star1 = get_next_XMAS_error(daily_list)
    print(f"First XMAS code error at: {star1}")
    star2_list = get_contiguous_codebreaking_list(star1, daily_list)
    star2_list.sort()
    print(star2_list)
    star2 = min(star2_list) + max(star2_list)
    print(f"Breaking pair's sum: {star2}")
    print(" --- BONUS: Any summands in list window ---")
    bonus_list = list(get_non_contigous_codebreaking_list(star1, daily_list))
    bonus_list.sort()
    print(bonus_list)
    print(sum(bonus_list))
    bonus_star = min(bonus_list) + max(bonus_list)
    print(f"Breaking pair any sum: {bonus_star}")

if __name__ == "__main__":
    main()


