import re
import numpy as np
import copy


def process(numbers,cnt):
        #starting numbers
        index = {}
        ix = 0

        while ix < len(numbers):
            index[numbers[ix]] = [ix]
            ix += 1

        while ix < cnt:
            #if ix % 300000 == 0:
            #    print(ix,cnt)
            #the ix number
            last = numbers[ix -1]
            #was last spoken? (exists in numbers)


            if(len(index[last]) >= 2):
                index[last] = index[last][:2]
                spoken = index[last][0] - index[last][1]
                numbers.append(spoken)
                if spoken not in index: index[spoken] = []
                index[spoken].insert(0,ix)
            else:
                #first time
                numbers.append(0)
                if 0 not in index: index[0] = []
                index[0].insert(0,ix)

            ix += 1

        #print("numbers",numbers)

        return numbers[-1]
