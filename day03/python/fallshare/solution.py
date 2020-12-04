from pathlib import Path
import re


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        data = list(map(list, f.read().splitlines()))

    return data

def get_map_height(data):
    return len(data)

def enhance_map(data, x_step, y_step):
    map_height = len(data)
    map_width = len(data[0])
    
    step_per_segment = map_width / x_step
    number_of_segments = int(map_height / (step_per_segment * y_step))

    for i in range(map_height):
        pattern = data[i]
        for j in range(number_of_segments):
            data[i] = data[i] + pattern

    return data

def traverse_map(data, x_step, y_step):
    x = 0
    y = 0
    height = len(data) - 1
    tree_count = 0

    while(y < height):     
        x += x_step
        y += y_step

        if data[y][x] == "#":
            tree_count += 1
    return tree_count
    

def analyze_slope(map, x_step, y_step):
    fullMap = enhance_map(data, x_step, y_step)
    return traverse_map(fullMap, x_step, y_step)



if __name__ == "__main__":
  
    mapTile = read_input_file('input.txt')

    tree_star1 = analyze_slope(mapTile, 3, 1)
    print(f"Star 1 - Number of trees is: {tree_star1}")

    slopes = ((1,1),(3,1),(5,1),(7,1),(1,2))
    tree_product = 1

    for slope in slopes:
        tree_count = analyze_slope(mapTile, slope[0], slope[1])
        print(f"slope: {slope} - trees: {tree_count}")
        tree_product *= tree_count

    print(f"Star 2 - Number of trees is: {tree_product}")