def getVersion():
    print("AoC2020_Day1!")

def read_file_to_list(filename):
    list = []
    file = open(filename, "r")
    for line in file:
        list.append(int(line))
    file.close()
    return list