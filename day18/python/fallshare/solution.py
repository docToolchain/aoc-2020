from pathlib import Path
import itertools
import math


def read_input_file(input_file_path):
    p = Path(input_file_path)
    equations = list()

    with p.open() as f:
        #split entries by blankline
        raw_equations = f.readlines()
        for raw_equation in raw_equations:
            raw_equation = raw_equation.strip()
            raw_equation = raw_equation.split(" ")
            equation = list()
            for term in raw_equation:
                if term.startswith("(") or term.endswith(")"):
                    equation += list(term)
                else:
                    equation.append(term)
            equations.append(equation)
    return equations

def get_right_closing_bracket(equation):
    left_bracket_count = 0

    for i in range(0, len(equation)):
        if equation[i] == ")":
            #check if last closing right bracket is found
            if left_bracket_count == 1:
                return i
            else:
                left_bracket_count -= 1
        if equation[i] == "(":
            left_bracket_count += 1
    return 0


def solve_star1(equation):
    while len(equation) != 1:
        if equation[0] == "(":
            left_bracket = 0
            right_bracket = get_right_closing_bracket(equation)
            #calculate result of equation
            result = solve_star1(equation[1:right_bracket])
            equation = equation[0:left_bracket] + list(result) + equation[right_bracket + 1:]
        elif equation[0].isdecimal():
            operand1 = int(equation[0])
            operator = equation[1]
            operand2 = 0
            if equation[2] == "(":
                left_bracket = 2
                right_bracket = get_right_closing_bracket(equation)
                operand2_last_index = right_bracket + 1
                operand2 = int(solve_star1(equation[3:right_bracket])[0])
                

            else:
                operand2 = int(equation[2])
                operand2_last_index = 3
            if operator == "+":
                result = str(operand1 + operand2)
            elif operator == "*":
                 result = str(operand1 * operand2)
            else:
                raise ValueError("this should never happen")

            equation = [result] + equation[operand2_last_index:]
                
        else:
            raise ValueError("this should never happen")
   
    return equation
        
def solve_star2(equation):
    #print(f"Start {equation}")
    while len(equation) != 1:
        if equation[0] == "(":
            left_bracket = 0
            right_bracket = get_right_closing_bracket(equation)
            #calculate result of equation
            result = solve_star2(equation[1:right_bracket])
            equation = equation[0:left_bracket] + list(result) + equation[right_bracket + 1:]
        elif equation[0].isdecimal():
            operand1 = int(equation[0])
            operator = equation[1]
            operand2 = 0

            if operator == "*":
                operand2_last_index = len(equation)
                operand2 = int(solve_star2(equation[2:])[0]) 
            elif equation[2] == "(":
                left_bracket = 2
                right_bracket = get_right_closing_bracket(equation)
                operand2_last_index = right_bracket + 1
                operand2 = int(solve_star2(equation[3:right_bracket])[0])              
            else:
                operand2 = int(equation[2])
                operand2_last_index = 3
            if operator == "+":
                #loese erste den rechten teil der gleichung
                result = str(operand1 + operand2)
            elif operator == "*":
                 result = str(operand1 * operand2)
            else:
                raise ValueError("this should never happen")

            equation = [result] + equation[operand2_last_index:]
                
        else:
            raise ValueError("this should never happen")
    #print(f"End {equation}")
    return equation


if __name__ == "__main__":

    equations  = read_input_file("input.txt")
    equation_sum = 0
    for equation in equations:
        #print(int(solve_star1(equation)[0]))
        equation_sum += int(solve_star1(equation)[0])
    
    print(f"Star 1: Sum off all equations is {equation_sum}")

    equation_sum = 0
    for equation in equations:
        #print(int(solve_star2(equation)[0]))
        equation_sum += int(solve_star2(equation)[0])
    
    print(f"Star 2: Sum off all equations is {equation_sum}")
    #print(f"Star 2: Solution is {get_last_number(start_numbers, 30000000)}")