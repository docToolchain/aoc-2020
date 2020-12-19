import math

def process_input(file_contents):
    lines_stripped = [line.strip() for line in file_contents]
    lines_stripped = [line.replace(" ","") for line in lines_stripped]

    return lines_stripped

def find_opening_par(input_string):
    position = input_string.rfind(")")
    counter = 1

    while counter > 0:
        position -= 1
        if input_string[position] == "(":
            counter -= 1
        elif input_string[position] == ")":
            counter += 1
    return position

def do_math(input_string):
    j = len(input_string) - 1
    if input_string[j] == ")":
        opening_par = find_opening_par(input_string)
        if input_string[opening_par-1] == "*":
            result = do_math(input_string[opening_par+1:j])*do_math(input_string[:opening_par-1])
        elif input_string[opening_par-1] == "+":
            result = do_math(input_string[opening_par+1:j])+do_math(input_string[:opening_par-1])
        else:
            return do_math(input_string[opening_par+1:j])
    else:
        number = int(input_string[j])
        if j>0:
            if input_string[j-1] == "*":
                result = number*do_math(input_string[:j-1])
            elif input_string[j-1] == "+":
                result = number+do_math(input_string[:j-1])
        else:
            result = number

    return result

def do_math2(input_string):
    last_par = input_string.rfind(")")
    while last_par != -1:
        opening_par = find_opening_par(input_string)
        input_string = input_string.replace(input_string[opening_par:last_par+1], str(do_math2(input_string[opening_par+1:last_par])))
        last_par = input_string.rfind(")")

    fragments = input_string.split("*")

    results = [sum([int(number) for number in fragment.split("+")]) for fragment in fragments]

    return math.prod(results)

def main():
    with open("input.txt",'r') as code_file:
        all_code_file = code_file.readlines()

    operations_list = process_input(all_code_file)

    math_results = [do_math(operation) for operation in operations_list]

    print("The sum of the answers to all problems in the initial homework is", sum(math_results))

    math_results = [do_math2(operation) for operation in operations_list]

    print("The sum of the answers to all problems in the advanced math homework is", sum(math_results))

main()

