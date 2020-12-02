
def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        # return_list = [int(item) for item in local_list] ## no casting on day02
        return local_list

def check_password_policy(single_line):
    ''' Checks single line for *both* password policies,
        returns a boolean tuple (old_policy_ok, current_policy_ok)'''
    # parse line_string
    line_splits = single_line.split(' ')
    numsies = line_splits[0].split('-')
    min_count_pos = int(numsies[0])
    max_count_pos = int(numsies[1])
    letter_required = line_splits[1][0]
    password = line_splits[2]

    count = 0
    new_policy = False
    #old_policy: check if letter count in range
    for i, c in enumerate(password):
        if (c == letter_required):
            count = count + 1
            # position is given in 'natural' numbers, thus subtract 1
            # current_policy: only one position must be the required letter
            if ((i == min_count_pos-1) or (i == max_count_pos-1)):
                new_policy = not new_policy
    old_policy = ((count >= min_count_pos) and (count <=max_count_pos))
    return (old_policy, new_policy)

daily_list = read_daily_input('input02.txt')
old_password_count = 0
current_password_count = 0
for line in daily_list:
    (old_yeah, current_yeah) = check_password_policy(line)
    if old_yeah: old_password_count += 1
    if current_yeah: current_password_count += 1

print("Old shop fine count: {}".format(old_password_count))
print("Current shop fine count: {}".format(current_password_count))

