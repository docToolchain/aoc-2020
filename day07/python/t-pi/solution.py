import math


def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [item.strip() for item in local_list]
        return return_list

def preprocess_daily_input(raw_list):
    bags = dict()
    for line in raw_list:
        bagsies = [element.strip() for element in line.split('contain')]
        color_outer = bagsies[0].split('bags')[0].strip()
        bags_inner = [element.strip() for element in bagsies[1].split(',')]
        colors_inner = list()
        for bag in bags_inner:
            if (not bag[0].isnumeric()): continue
            amount = int(bag[0])
            color = bag[2:bag.find('bag')].strip()
            colors_inner.append((color, amount))
        if (color_outer in bags.keys()):
            colors_inner = list(set(colors_inner).union(set(bags[color_outer])))
        bags[color_outer] = colors_inner
    return bags

def get_color_nesting_options(bags_dict, my_color, all_nested_colors = set()):
    nesting_colors = []
    nesting_options = 0
    for outer, inner_list in bags_dict.items():
        for colors in inner_list:
            if ((my_color == colors[0]) and (outer not in all_nested_colors)):
                nesting_colors.append(outer)
                all_nested_colors.add(outer)
    nesting_options += len(nesting_colors)
    for color in nesting_colors:
        nesting_options += get_color_nesting_options(bags_dict, color, all_nested_colors)
    return nesting_options

def get_nested_bags(bags_dict, my_color, my_count, all_nested_colors = set()):
    nested_bags = my_count
    if (my_count == 0): my_count = 1
    for outer, inner_list in bags_dict.items():
        if (outer == my_color):
            for color, amount in inner_list:
                if (amount > 0):
                    nested_bags += get_nested_bags(bags_dict, color, my_count*amount, all_nested_colors)
    return nested_bags


def main():
    daily_list = read_daily_input('input07.txt')
    bags = preprocess_daily_input(daily_list)
    star1 = get_color_nesting_options(bags, 'shiny gold')
    print(f"{star1} bags can hold my 'shiny gold' bag")
    star2 = get_nested_bags(bags, 'shiny gold', 0)
    print(f"My 'shiny gold' bag holds {star2} bags")

if __name__ == "__main__":
    main()


