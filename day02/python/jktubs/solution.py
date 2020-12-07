import utils

utils.getVersion()

input = utils.read_file_to_list("input.txt")

#print(input)

size = len(input)
print("len: {}".format(size))
valid_passwords_policy1 = 0
valid_passwords_policy2 = 0
for i in input:
    pos1 = i.find("-")
    pos2 = i.find(" ")
    pos3 = i.find(":")
    #print("pos1: {}, pos2: {}, pos3: {}".format(pos1, pos2, pos3))
    num_min = int(i[0:pos1])
    num_max = int(i[pos1+1:pos2])
    letter = i[pos2+1:pos3]
    password = i[pos3+2:]
    print("num_min: {}, num_max: {}, letter: {}, password: {}".format(num_min, num_max, letter, password))
    count = password.count(letter)
    print("count: {}".format(count))
    if count >= num_min and count <= num_max:
        valid_passwords_policy1 += 1
        print("valid_passwords_policy1")

    size_psw = len(password)
    if (num_min-1 < size_psw) and (num_max-1 < size_psw):
        if (password[num_min-1] == letter or password[num_max-1] == letter):
            if password[num_min-1] != password[num_max-1]:
                valid_passwords_policy2 += 1
                print("valid_passwords_policy2")
            else:
                print('both letters are the same ==> invalid policy2')

    print(i)

print("part 1: password policy valid for: {}".format(valid_passwords_policy1))
print("part 2: password policy valid for: {}".format(valid_passwords_policy2))

    


# for i in range(0, size):
#     for j in range(0, size):
#         if i != j:
#             sum = input[i] + input[j]
#         else:
#             sum = 0
#         if sum == 2020:
#             print("sum = {}, i = {}, j = {}, val1 = {}, val2 = {}, multiplication = {}".format(sum,i,j,input[i],input[j],input[i]*input[j]))


