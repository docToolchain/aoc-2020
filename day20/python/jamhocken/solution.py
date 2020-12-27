import numpy
import math
import re

def process_input(file_contents):
    line = 0
    edges = dict()
    elements = dict()
    while line < len(file_contents):
        vector2 = str()
        vector4 = str()
        core = list()

        tile_no = int(file_contents[line].strip(" Tile:\n"))

        line += 1
        vector1 = file_contents[line].strip()
        vector3 = file_contents[line+len(vector1)-1].strip()[::-1]
        for i in range(line,line+len(vector1)):
            vector2 += file_contents[i][len(vector1)-1]
            vector4 += file_contents[i][0]
            core.append(file_contents[i].strip())
        vector4 = vector4[::-1]

        edges.update({tile_no: [vector1,vector2,vector3,vector4]})
        elements.update({tile_no: core})
        line += len(vector1)+1

    return edges, elements

def visualize_element(element):
    for strings in element:
        print(strings)
    print()

def find_neighbors(borders):
    neighborhood = dict()
    sides = dict()
    for key, strings in borders.items():
        neighbors = list()
        side_list = list()
        for j, string in enumerate(strings):
            match = 0
            for key1, strings1 in borders.items():
                if key1 != key:
                    for k, string1 in enumerate(strings1):
                        if string == string1:
                            match = key1
                            side = j
                        if string == string1[::-1]:
                            match = key1
                            side = j
            if match != 0:
                neighbors.append(match)
                side_list.append((match,side))
        neighborhood[key] = neighbors
        sides[key] = side_list
    
    return neighborhood, sides

def problem1(neighborhood):
    product = 1
    for key, element in neighborhood.items():
        if len(element) == 2:
            product *= key
    
    return product

def reorient_element(element1,element2):
    vectors1 = [element1[0],"".join([x[len(element1)-1] for x in element1]),element1[len(element1)-1][::-1],"".join([x[0] for x in element1])[::-1]]
    vectors2 = [element2[0],"".join([x[len(element2)-1] for x in element2]),element2[len(element2)-1][::-1],"".join([x[0] for x in element2])[::-1]]
    
    for j, string in enumerate(vectors1):
        for k, string1 in enumerate(vectors2):
            if string == string1:
                if j == k:
                    if j % 2 == 1:
                        transformation = 6
                    else:
                        transformation = 4
                elif (j - k) % 2 == 0:
                    if j % 2 == 1:
                        transformation = 4
                    else:
                        transformation = 6
                elif (j - k) % 4 == 1:
                    if k % 2 == 0:
                        transformation = 5
                    else:
                        transformation = 7
                else:
                    if k % 2 == 0:
                        transformation = 7
                    else:
                        transformation = 5
            if string == string1[::-1]:
                if j == k:
                    transformation = 2
                else:
                    if (j-k)%2==0:
                        transformation = 0
                    elif (j-k)%4 == 1:
                        transformation = 3
                    else:
                        transformation = 1
                    
    return transform_element(element2, transformation)

def create_image(neighborhood, cores):
    corners = [key for key, value in neighborhood.items() if len(value)==2]
    edges = [key for key, value in neighborhood.items() if len(value)==3]

    frame = set(corners + edges)
    frame.remove(corners[0])    
    resolved_elements = {corners[0]}
    current_element = corners[0]
    graph = [corners[0]]
    corners.pop(0)
    # Create "first" row of overall image
    while current_element not in corners:
        for element in neighborhood[current_element]:
            if element in frame:
                graph.append(element)
                frame.remove(element)
                resolved_elements.add(element)
                cores[element] = reorient_element(cores[current_element], cores[element])                                                                               
                current_element = element
                break

    # Finish the graph one row at a time
    while resolved_elements != set(cores.keys()):
        graph1 = graph.copy()
        for member in graph1:
            for element in neighborhood[member]:
                if element not in resolved_elements:
                    graph.append(element)
                    resolved_elements.add(element)
                    cores[element] = reorient_element(cores[member], cores[element])                                                                               
                    current_element = element
                    break

    return cores, graph

def transform_element(element, code):
    if code == 1:
        return rotate_piece(element,1)
    elif code == 2:
        return rotate_piece(element,2)
    elif code == 3:
        return rotate_piece(element,3)
    elif code == 4:
        return flip_piece(element)
    elif code == 5:
        return rotate_piece(flip_piece(element),1)
    elif code == 6:
        return rotate_piece(flip_piece(element),2)
    elif code == 7:
        return rotate_piece(flip_piece(element),3)
    else:
        return element
    
def rotate_piece(strings,times):
    return list([''.join(numpy.rot90(numpy.array([list(i) for i in strings]), -1*times)[j]) for j in range(len(strings))])

def flip_piece(strings):
    return list([''.join(numpy.flipud(numpy.array([list(i) for i in strings]))[j]) for j in range(len(strings))])

def main():
    with open("input.txt",'r') as code_file:
        all_code_file = code_file.readlines()

    borders, elements = process_input(all_code_file)
    
    neighborhood, sides = find_neighbors((borders))

    print("The product of the 4 corner pieces is", problem1(neighborhood))

    image, graph = create_image(neighborhood.copy(),elements.copy())     

    width = int(round(math.sqrt(len(graph))))
    width1 = len(elements[graph[0]])

    # rotate to put the first element of graph in the top left corner
    transformation_code = (1-sides[graph[0]][0][1])%4
    if (sides[graph[0]][0][1] - sides[graph[0]][1][1])%4 == 1:
        transformation_code += 4

    # # strip the borders and transform each element
    new_cores = image.copy()            
    for key,values in image.items():
        values = transform_element(values, transformation_code)
        new_element = list()
        for j, string in enumerate(values):
            if j != 0 and j != width1-1:
                new_element.append(string[1:width1-1])
        new_cores.update({key: new_element})

    ## Put the pieces together to make the total image
    big_room = list()
    for i in range(width):
        big_room += new_cores[graph[i*width]]
        for j in range(width*i+1,width*(i+1)):
            for k in range((width1-2)*i,(width1-2)*(i+1)):
                big_room[k] = big_room[k] + new_cores[graph[j]][k-(width1-2)*i]

    count = 0
    transformation = 0
    sea_monster_width = 20
    big_width = (width1-2)*width-sea_monster_width
    # loop until the orientation is correct
    while count == 0:
        new_big_room = transform_element(big_room, transformation)
        one_string = "".join(new_big_room)
        count = 0
        regex = re.compile(fr"(?=(..................#..{{{big_width}}}#....##....##....###.{{{big_width}}}.#..#..#..#..#..#...))")
        iterator = regex.finditer(one_string)
        for hits in iterator:
            count += 15
        transformation += 1
        
    count1 = 0
    for line in new_big_room:
        for character in line:
            if character == "#":
                count1 += 1
    
    print("The sea roughness is",count1- count)
            
main()