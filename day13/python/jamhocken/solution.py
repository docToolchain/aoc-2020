import re

def process_input(input_line):
    stripped_input = input_line.rstrip()
    raw_list = re.split(',',stripped_input)
    times = list()
    for j,i in enumerate(raw_list):
        if i == 'x': pass
        else: times.append((int(i),j))
    return times

with open("bus_schedule.txt", 'r') as code_file:
    earliest_dep = code_file.readline()
    earliest_dep.rstrip()
    earliest_dep = int(earliest_dep)
    schedule = process_input(code_file.readline())

bus_wait = [bus[0] - earliest_dep % bus[0] for bus in schedule]
my_bus = bus_wait.index(min(bus_wait))

print('The ID of the earliest bus I can take is', schedule[my_bus][0])
print('I will have to wait', bus_wait[my_bus], 'minutes for it')
print('The product of those 2 numbers is', schedule[my_bus][0]*bus_wait[my_bus])

ref_time = schedule[0][0]
time_fixed = 0
for bus in schedule:
    i = 0
    while (time_fixed+ref_time*i + bus[1]) % bus[0] != 0:
            i += 1
    time_fixed = time_fixed + ref_time*i
    if bus[1] != 0:
        ref_time = ref_time*bus[0]

print('Problem 2: The earliest valid timestamp is', time_fixed)
