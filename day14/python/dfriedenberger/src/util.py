import re
import numpy as np


def read_file_to_list(filename):
        """Read file to map"""
        rows = []
        file = open(filename, "r")
        for line in file:
            m = re.search(r'^mask\s+=\s+([01X]+)$', line)
            if m: 
                rows.append({"type" : "mask" , "mask": m.group(1)})
                continue
            m = re.search(r'mem\[([0-9]+)\]\s+=\s+([0-9]+)$', line)
            if m: 
                rows.append({"type" : "mem" , "address": int(m.group(1)), "value" : int(m.group(2))})
                continue
            raise Exception(line)
        return rows

def process(mask,value):
        nvalue = 0
        for i in range(36):
            if mask[35 - i] == '0':
                v = 0
            if mask[35 - i] == '1':
                v = 1
            if mask[35 - i] == 'X':  
                v = value >> i & 1
            #print(i,mask[35 - i],v,pow(2,i))
            nvalue +=  v * pow(2,i)
        return nvalue

def process_address(mask,address):
        nvalue = [0]
        for i in range(36):
            if mask[35 - i] == '0':
                for x in range(len(nvalue)):
                    nvalue[x] += (address >> i & 1)  * pow(2,i)
            if mask[35 - i] == '1':
                for x in range(len(nvalue)):
                    nvalue[x] += pow(2,i)
            if mask[35 - i] == 'X':
                l = []
                for value in nvalue:
                    l.append(value)
                    l.append(value + pow(2,i))
                nvalue = l
        return nvalue