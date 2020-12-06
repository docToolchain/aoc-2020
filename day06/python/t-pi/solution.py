import math

def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [item.strip() for item in local_list]
        return return_list

def get_groups_answers(answers_list, star = 2):
    ''' Collect answers of a passenger batch and return sum
        star = 1: Collect any answer from any group's passenger
        star = 2: Collect only answers that are in all passengers' answers
    '''
    group_answers = list()
    found_answers = list()
    answers_sum = 0
    group_answer_sum = 0
    for line in answers_list:
        if (len(line) == 0):
            answers_sum += len(found_answers)
            group_answer_sum += len(group_answers)
            found_answers = list()
            group_answers = list()
            continue
        if (len(found_answers) == 0):
            group_answers = list(line)
        # star == 1
        for letter in line:
            if (letter not in found_answers):
                found_answers.append(letter)
        # star == 2
        pop_me = list()
        for letter in group_answers:
            if (letter not in line):
                pop_me.append(letter)
        for pop_letter in pop_me:
            group_answers.pop(group_answers.index(pop_letter))
    if (len(found_answers) > 0):
        answers_sum += len(found_answers)
        found_answers = list()
    if (len(group_answers) > 0):
        group_answer_sum += len(group_answers)
        group_answer = list()
    if (star == 1): 
        return answers_sum
    return group_answer_sum


def main():
    daily_list = read_daily_input('input06.txt')
    print(f"The sum of all group answers is {get_groups_answers(daily_list, 1)}")
    print(f"The sum of joint group answers is {get_groups_answers(daily_list, 2)}")
    print("The answer to life, universe and everything is 42")

if __name__ == "__main__":
    main()


