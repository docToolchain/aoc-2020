
import re
import copy

def read_file_to_list(filename):
    """Read file to List"""
    list = []
    file = open(filename, "r")
    for line in file:
            list.append(int(line.strip()))
    file.close()
    return list

class NumberCache():

    def __init__(self, preambel):
        self._preambel = preambel
        self._sum = []

    def add(self,number):

        if len(self._sum) >= self._preambel:
            self._sum.pop(0)
            for i in range(self._preambel - 1):
                self._sum[i].pop(1)

        #calculate 
        sum = [ number ]
        for i in range(len(self._sum)):
            sum.append(self._sum[i][0] + number)
        self._sum.append(sum)
        return

    def valid(self,number):
        for i in range(self._preambel):
            for x in range(1,len(self._sum[i])):
                if self._sum[i][x] == number:
                    return True
        return False


        