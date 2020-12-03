correct_passwords_rule_1 = 0
correct_passwords_rule_2 = 0

with open("password_file.txt",'r') as password_file: 
    for line in password_file:

        step_0 = line.split()
        step_1 = step_0[0].split('-')
        
        min_number = int(step_1[0])
        max_number = int(step_1[1])
        necessary_character = step_0[1].strip(':')
        string_to_check = step_0[2]

        # Check Rule 1
        txt_count = string_to_check.count(necessary_character)
        if min_number <= txt_count <= max_number: correct_passwords_rule_1 += 1 
        
        #Check Rule 2
        if string_to_check[min_number-1] == necessary_character:
            if string_to_check[max_number-1] != necessary_character:
                correct_passwords_rule_2 += 1
        else:
            if string_to_check[max_number-1] == necessary_character:
                correct_passwords_rule_2 += 1
        
print('There are', correct_passwords_rule_1, 'correct passwords \
according to rule 1.')

print('There are', correct_passwords_rule_2, 'correct passwords \
according to rule 2.')