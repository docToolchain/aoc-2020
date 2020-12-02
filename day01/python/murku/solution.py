def fix_expense_report(list_of_expenses):
    """
    brute force solution
    and expecting an ideal dataset i.e. one and only one pair is exists
    """
    for i in range(len(list_of_expenses)):
        for j in range(i, len(list_of_expenses)):
            summ = list_of_expenses[i] + list_of_expenses[j]
            if  summ == 2020:
                print(list_of_expenses[i], list_of_expenses[j])
                return list_of_expenses[i]*list_of_expenses[j]

def read_in_input(filename):
    """
    reads in the input from a txt
    """
    file_handle = open(filename, 'r')
    numbers_as_str = file_handle.read().splitlines()
    return  list(map(int, numbers_as_str))
    
if __name__ == "__main__":
    # training_set = [1721, 979, 366, 299, 675, 1456]
    # pairs_to_find = [299, 1721]
    # expected_result = 514579
    # print(fix_expense_report(training_set))

    # problem_input = read_in_input('test.txt')
    problem_input = read_in_input('ProblemInput.txt')
    # print(problem_input)
    print(fix_expense_report(problem_input))

