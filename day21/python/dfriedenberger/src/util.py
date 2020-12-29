import re
import math
import copy


def read_file_to_list(filename):
        """Read file to map"""
        foods = []
        
        file = open(filename, "r")
        for line in file:
            line = line.strip()
            if line == "": continue

            #mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
            m = re.search(r'^(.*)[(]contains(.*)[)]$', line)
            if not m: raise Exception(line)
            ingredients = m.group(1).strip().split(" ")
            allergens =  [x.strip(' ') for x in m.group(2).strip().split(",")] 
            foods.append({"ingredients" : set(ingredients) , "allergens" : set(allergens)})


        return foods


