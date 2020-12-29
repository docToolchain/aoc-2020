#!/usr/bin/env python3
from src.util import *

# tag::starOne[]
foods = read_file_to_list("input.txt")

l = len(foods)
dangerous = dict()
while True:
    allergens = dict()
    for i in range(l):
        if len(foods[i]["allergens"]) == 1:
            allg = list(foods[i]["allergens"])[0]
            if allg not in allergens: allergens[allg] = set(foods[i]["ingredients"])
            else: allergens[allg].intersection_update(foods[i]["ingredients"])

        for j in range(i+1,l):
            ingr = foods[i]["ingredients"] & foods[j]["ingredients"]
            allerg = foods[i]["allergens"] & foods[j]["allergens"]
            if len(allerg) == 1:
                allg = list(allerg)[0]
                if allg not in allergens: allergens[allg] = set(ingr)
                else: allergens[allg].intersection_update(ingr)
    
    reduce = False
    for allg in allergens.keys():
        if len(allergens[allg]) == 1:
            ingr = list(allergens[allg])[0]
            #print(ingr +" has "+allg)
            dangerous[allg] = ingr
            reduce = True
            for food in foods:
                food["ingredients"].discard(ingr)
                food["allergens"].discard(allg)
    if not reduce: break

rest = []
for food in foods:
    if len (food["allergens"]) != 0: raise Exception(food)
    rest += list(food["ingredients"])

print(len(rest))
# end::starOne[]

# tag::starTwo[]
dangerousList = []
for k in sorted(dangerous.keys()):
    dangerousList.append(dangerous[k])

print(','.join(dangerousList))
# end::starTwo[]
