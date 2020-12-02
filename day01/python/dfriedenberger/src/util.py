


def read_file_to_list(filename):
    """Read file to List"""
    list = []
    file = open(filename, "r")
    for line in file:
        intval = int(line)
        list.append(intval)
    file.close()
    return list

