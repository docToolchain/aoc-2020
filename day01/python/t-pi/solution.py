def iterate_stupidly_x3(expenses):
    """ Stupidly iterate three times through the given list
        and check for the correct sum of 2020 """
    for i1, n1 in enumerate(expenses):
        for i2, n2 in enumerate(expenses[i1:]):
            for i3, n3 in enumerate(expenses[i2:]):
                if (int(n1)+int(n2)+int(n3) == 2020):
                    print(int(n1)*int(n2)*int(n3))
                    return

with open('input.txt') as input_file:
    expenses_list = input_file.readlines()

iterate_stupidly_x3(expenses_list)
