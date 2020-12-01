
def search_expenses(expenses):
    match_of_two_found = False
    match_of_three_found = False
    for first_index, first_expense in enumerate(expenses):
        for second_index, second_expense in enumerate(expenses[first_index+1:]):
            sum_of_two = int(first_expense) + int(second_expense)

            if sum_of_two == 2020:
                product = int(first_expense) * int(second_expense)
                print(f"Hey, found a match:\n {first_expense} * {second_expense} = {product}")
                match_of_two_found = True

            for third_expense in expenses[second_index+1:]:
                sum_of_three = int(first_expense) + int(second_expense) + int(third_expense)

                if sum_of_three == 2020:
                    product = int(first_expense) * int(second_expense) * int(third_expense)
                    print(f"Hey, found a match:\n {first_expense} * {second_expense} * {third_expense} = {product}")
                    match_of_three_found = True
                    
        if match_of_two_found & match_of_three_found:
            return
    print("Sorry, but no match found :-(")


with open('expenseReport.txt') as expense_report:
    expenses = expense_report.readlines()

#search_two_expenses(expenses)

search_expenses(expenses)

