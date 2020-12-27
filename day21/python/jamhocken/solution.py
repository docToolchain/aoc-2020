from copy import deepcopy

def process_input(file_contents):
    food = list()
    ingredients = set()
    allergens = set()
    for line in file_contents:
        split_line = line.split("(")
        ingredient_temp = split_line[0].strip().split(" ")
        allergen_temp = split_line[1].strip(")\n").split(" ")
        allergen_temp.remove("contains")
        allergen_temp = list([allergen.replace(",","") for allergen in allergen_temp])
        allergens.update(set(allergen_temp))
        ingredients.update(set(ingredient_temp))
        food.append((set(ingredient_temp), set(allergen_temp)))
    return food, ingredients, allergens

def find_excludedict(foods, ingredients):
    excludedict = dict()
    for ingredient in ingredients:
        exclusionset = set()
        for food in foods:
            if ingredient not in food[0]:
                exclusionset.update(food[1])
        excludedict.update({ingredient: exclusionset})

    return excludedict

def cleanup_foodlist(nonallergic, foods):
    occurred = 0
    cleaned_food_list = deepcopy(foods)
    for ingredients in nonallergic:
        for j,food in enumerate(foods):
            for food_ingredient in food[0]:
                if food_ingredient == ingredients:
                    occurred += 1
                    cleaned_food_list[j][0].remove(food_ingredient)

    return cleaned_food_list, occurred

def create_matchingdict(allergens,foods):
    match_dict = dict()
    for allergene in allergens:
        ingredients = set()
        for food in foods:
            for food_allergene in food[1]:
                if food_allergene == allergene:
                    if ingredients == set():
                        ingredients = food[0]
                    else:
                        ingredients = ingredients.intersection(food[0])
        match_dict.update({allergene: ingredients})

    return match_dict

def main():
    with open("food.txt",'r') as code_file:
        all_code_file = code_file.readlines()

    foods, ingredients, allergens = process_input(all_code_file)

    excludedict = find_excludedict(foods, ingredients)

    nonallergic = {ingredient for ingredient in ingredients if len(excludedict[ingredient]) == len(allergens)}
    
    cleaned_food_list, occurances = cleanup_foodlist(nonallergic, foods)

    print("The ingredients without any allergens occurred", occurances,"times.")

    match_dict = create_matchingdict(allergens, cleaned_food_list)

    solved = dict()
    while len(solved) < len(allergens):
        temp_dict = deepcopy(match_dict)
        values = set()
        for key, value in match_dict.items():
            if len(value) == 1:
                solved.update({key:value})
                temp_dict.pop(key)
                values.update(value)
        match_dict = deepcopy(temp_dict)
        for key,value in match_dict.items():
            temp_dict[key].difference_update(values)
        match_dict = temp_dict

    print("The canonical dangerous ingredient list is (don't copy the last comma...)")
    for key in sorted(solved):
        print(list(solved[key])[0],end=",")

main()