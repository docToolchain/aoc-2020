from pathlib import Path
import re

def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        #split entries by blankline
        raw_data_groups = f.read().split("\n\n")

        groups = []
        
        for raw_group in raw_data_groups:
            #normalize entry by removing new lines
            passengers = raw_group.strip().split("\n")
            group = []
            for passenger in passengers:
                group.append(set(passenger))
            groups.append(group) 

    return groups

def solution_star1(groups):
    totalCount = 0

    for group in groups:
        super_set = set()
        for passenger in group:
            super_set = super_set.union(passenger)
        
        totalCount += len(super_set)
    return totalCount

def solution_star2(groups):
    totalCount = 0

    for group in groups:
        intersection_set = group[0]
        for passenger in group:
            intersection_set = intersection_set.intersection(passenger)
        
        totalCount += len(intersection_set)
    return totalCount

if __name__ == "__main__":

    groups = read_input_file('input.txt')
    print(f"Star 1 - Solution: {solution_star1(groups)}")
    print(f"Star 2 - Solution: {solution_star2(groups)}")