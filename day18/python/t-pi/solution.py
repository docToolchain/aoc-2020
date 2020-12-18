# see README.doc

import re


def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [item.strip() for item in local_list]
        return return_list


def evaluate_straight(expression):
    ''' String expression evaluation from left to right.
        Returns result as int
        No parentheses allowed!
    '''
    result = 0
    elements = expression.split(' ')
    operator = ''
    for element in elements:
        if (element.isnumeric()):
            value = int(element)
            if (operator == '*'):
                result *= value
            else:
                result += value
        else:
            operator = element
    return result


def evaluate_advanced(expression):
    ''' String expression evaluation "plus" first, then the rest.
        Returns result as int
        No parentheses allowed!
    '''
    elements = expression.split(' ')
    while (plusses_count := elements.count('+') > 0):
        next_plus = elements.index('+')
        summy = int(elements[next_plus-1]) + int(elements[next_plus+1])
        elements[next_plus] = str(summy)
        del elements[next_plus+1]
        del elements[next_plus+-1]
        expression = " ".join(c for c in elements)
    result = evaluate_straight(expression)
    return result


def evaluate_parentheses(expression, star):
    ''' Crawl through string expression for parenthesis levels.
        Evaluates innermost first with other evaluation functions, depending on star level.
        Returns result as int.
        Parentheses allowed.
    '''
    evaluate = evaluate_straight
    if (star == 2):
        evaluate = evaluate_advanced
    while (max_level := expression.count('(') > 0):
        level = 0
        p_level = list()
        for idx, c in enumerate(expression):
            if (c == '('):
                level += 1
            if (c == ')'):
                level -= 1
            p_level.append(level)
        max_level = max(p_level)
        p_level = "".join([str(c) for c in p_level])
        left = p_level.find(str(max_level))
        right = left + p_level[left+1:].find(str(max_level-1)) + 2
        sub_result = evaluate(expression[left:right].strip('()'))
        expression = expression[:left] + str(sub_result) + expression[right:]
    result = evaluate(expression)
    return result


def evaluate_parentheses_smart(expression, star):
    ''' Crawl through string expression for parentheses.
        Inspiration from repo colleagues: start with closing parenthesis. Makes it much easier :)
        Returns result as int.
        Parentheses allowed.
    '''
    evaluate = evaluate_straight
    if (star == 2):
        evaluate = evaluate_advanced
    while (max_level := expression.count(')') > 0):
        right = expression.find(')')
        left = expression[:right].rfind('(')
        sub_result = evaluate(expression[left:right].strip('()'))
        expression = expression[:left] + str(sub_result) + expression[right+1:]
    result = evaluate(expression)
    return result


def do_the_maths(expression_list, star=1):
    ''' Iterate through the homework list and sums up the line results
    '''
    math_sum = 0
    for line in expression_list:
        math_sum += evaluate_parentheses_smart(line, star)
    return math_sum


def main():
    daily_list = read_daily_input('input18.txt')
    star1 = do_the_maths(daily_list)
    print(f"Result (*): {star1}")
    star2 = do_the_maths(daily_list, star=2)
    print(f"Result (**): {star2}")


if __name__ == "__main__":
    main()
