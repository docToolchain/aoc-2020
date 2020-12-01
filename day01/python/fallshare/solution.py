with open('input.txt') as input_file:
    input = []
    for line in input_file:
        input.append(int(line.strip('\n')))

assert int(input[0]) == 408

def findNumber_Star1(input):
    for x in input:        
        subList = input.copy()
        subList.pop(0)
        for y in subList:
            sum = x + y
            if(sum == 2020):
                print(f"{x} + {y} = {x + y}")
                return x * y

    return "No match found"


def findNumber_Star2(input):
    for x in input:     
        subList = input.copy()
        subList.pop(0)
        for y in subList:
            sublist2 = subList.copy()
            sublist2.pop(0)
            for z in sublist2:
                sum = x + y + z
                if(sum == 2020):
                    print(f"{x} + {y} = {x + y + z}")
                    return x * y * z

    return "No match found"


print("Star 1: " + str(findNumber_Star1(input)))
print("Star 2: " + str(findNumber_Star2(input)))               