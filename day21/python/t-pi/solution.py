# see README.doc

import re
from pprint import pprint


def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [item.strip() for item in local_list]
        return return_list


def preprocess_input(daily_list):
    ''' Reads input into a food list [set(food), set(allergenes)]
        Returns food list, set(all_foods), set(all_allergenes)
    '''
    food_list = list()
    all_allergenes = set()
    all_foods = set()
    for line in daily_list:
        ingreds, allergs = line.split('(contains')
        ingredients = {word for word in ingreds.strip().split(' ')}
        all_foods.update(ingredients)
        allergenes = [word for word in allergs.strip(' )').split(', ')]
        all_allergenes.update(allergenes)
        food_list.append((ingredients, allergenes))
    return food_list, all_foods, all_allergenes


def identify_allergenes(food_list, all_foods, all_allergenes):
    ''' Sieve food list by intersecting all food sets per allergene.
        Then filter the allergenes from the unique relations, as on day 16
        Returns dict {'english_name': {unique garbled name}}
    '''
    allergenes_list = dict()
    for allerg in all_allergenes:
        allerg_food = [food[0] for food in food_list if allerg in food[1]]
        allergs_found = all_foods.intersection(*allerg_food)
        allergenes_list[allerg] = allergs_found
    done = False
    while (done == False):
        done = True
        for a, names in allergenes_list.items():
            if (len(names) == 1):
                name = next(iter(names))
                for sub_idx, sub_names in allergenes_list.items():
                    if (sub_idx == a):
                        continue
                    if (name in sub_names):
                        done = False
                        allergenes_list[sub_idx].remove(name)
    return allergenes_list


def main():
    daily_list = read_daily_input('input21.txt')
    food_list, all_foods, all_allergenes = preprocess_input(daily_list)
    allergenes_list = identify_allergenes(food_list, all_foods, all_allergenes)
    critical_food = set.union(*allergenes_list.values())
    free_food = {food for food in all_foods if food not in critical_food}
    star1 = sum([len(set.intersection(food, free_food))
                 for food, allerg in food_list])
    print(f"Result (*): {star1}")

    english_allergene_list = list(allergenes_list.keys())
    english_allergene_list.sort()
    pprint(english_allergene_list)
    pprint(allergenes_list)
    print(f"Result(**): ",
          ",".join([next(iter(allergenes_list[a]))
                    for a in english_allergene_list]))


if __name__ == "__main__":
    main()
