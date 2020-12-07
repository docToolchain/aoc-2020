def getVersion():
    print("AoC2020_Day2!")

def read_file_to_list(filename):
    list = []
    file = open(filename, "r")
    for line in file:
        list.append(line.strip())
    file.close()
    return list