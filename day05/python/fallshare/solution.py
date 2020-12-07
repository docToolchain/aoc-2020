from pathlib import Path
import re

def read_input_file(input_file_path):
    p = Path(input_file_path)

    boarding_passes = []
    with p.open() as input_file:
   
        for line in input_file:
            #replace characters with 0 and 1 to get binary representation
            binary_representation = line.replace("B","1").replace("F","0").replace("L","0").replace("R","1").strip()

            boarding_pass = dict()

            boarding_pass["row"] = int(binary_representation[0:7],2)
            boarding_pass["column"] = int(binary_representation[7:10],2)
            boarding_pass["seat_id"] = int(binary_representation,2)

            boarding_passes.append(boarding_pass)

    return boarding_passes

def get_highest_seat_id(boarding_passes):
    seat_ids = set()
    for boarding_pass in boarding_passes:
        seat_ids.add(boarding_pass["seat_id"])
    return max(seat_ids)

def find_free_seat(boarding_passes):    
    #a list of all taken seats
    occupied_seats = set()
    for boarding_pass in boarding_passes:
        occupied_seats.add(boarding_pass["seat_id"])
    
    seat_map = set(range(0,1024))
   
    free_seats = seat_map.difference(occupied_seats)

    #removing front and back row
    free_seats = free_seats.intersection(set(range(8,1016)))

    for seat_id in free_seats:
        if ((seat_id - 1) not in free_seats) and ((seat_id + 1) not in free_seats):
            return seat_id
 
if __name__ == "__main__":
    boarding_passes = read_input_file("input.txt")
    print(f"Star 1: Highest seat id: {get_highest_seat_id(boarding_passes)}")
    print(f"Star 2: Free seat id: {find_free_seat(boarding_passes)}")