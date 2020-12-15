import utils

utils.getVersion()

input = utils.read_file_to_list("input.txt")

# print(input)

size = len(input)
utils.log.debug("len: {}".format(size))

seats=[]
seats = [i for i in range(127*8+8)]
max_seat_id = 0
for i in range(0, size):
    seat_id = utils.get_seat_id(input[i])
    seats[seat_id] = 'X'
    if seat_id > max_seat_id:
        max_seat_id = seat_id

utils.log.info("solution part 1 ==> max_seat_id: {}".format(max_seat_id)) # ==> 928

possible_seats = 0
my_seat = -1
for i in range(0, len(seats)):
    if 1 < i < len(seats):
        if seats[i-1] == 'X' and seats[i+1] == 'X' and seats[i] != 'X':
            utils.log.debug("empty seat: {}".format(seats[i]))
            my_seat = seats[i]
            possible_seats += 1

if possible_seats == 1:
    utils.log.info("solution part 2 ==> my_seat: {}".format(my_seat)) # ==> 610
else:
    utils.log.warning("solution part 2 ==> possible_seats: {} ==> not unique".format(possible_seats))

