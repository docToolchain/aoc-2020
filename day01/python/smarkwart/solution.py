
def search_two_expenses(expenses):
    for index, first_expense in enumerate(expenses):
        for second_expense in expenses[index+1:]:
            sum = int(first_expense) + int(second_expense)
            if sum == 2020:
                product = int(first_expense) * int(second_expense)
                print(f"Hey, found a match:\n {first_expense} * {second_expense} = {product}")
                return
    print("Sorry, but no match found :-(")

def search_three_expenses(expenses):
    for first_index, first_expense in enumerate(expenses):
        for second_index, second_expense in enumerate(expenses[first_index+1:]):
            for third_expense in expenses[second_index+1:]:
                sum = int(first_expense) + int(second_expense) + int(third_expense)
                if sum == 2020:
                    product = int(first_expense) * int(second_expense) * int(third_expense)
                    print(f"Hey, found a match:\n {first_expense} * {second_expense} * {third_expense} = {product}")
                    return
    print("Sorry, but no match found :-(")

with open('expenseReport.txt') as expense_report:
    expenses = expense_report.readlines()

search_two_expenses(expenses)

search_three_expenses(expenses)

