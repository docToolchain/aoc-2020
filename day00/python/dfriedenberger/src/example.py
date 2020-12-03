


def read_file_to_list(filename):
    """Read file to List"""
    list = []
    file = open(filename, "r")
    for line in file:
        intval = int(line)
        list.append(intval)
    file.close()
    return list




class Example():

    def __init__(self, name):
        self._name = name
        

    @property
    def name(self):
        return self._name

    def get_name(self):
        return self._name