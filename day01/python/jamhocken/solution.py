with open("expenses.txt",'r') as expense_report:
    
    values = list(map(int,expense_report))
    values2 = values.copy()

    for expense in values:
        values2.remove(expense)
        values3 = values2.copy()
        for expense2 in values2:
            if expense + expense2 == 2020:
                print(expense, ' + ', expense2, ' = 2020.')
                print('Their product is ', expense*expense2)
            values3.remove(expense2)
            for expense3 in values3:
                if (expense + expense2 + expense3) == 2020:
                    print(expense,' + ',expense2,' + ',expense3,' = 2020.')
                    print('Their product is ', expense*expense2*expense3)    