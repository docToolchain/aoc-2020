# see README.doc

import math


def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [(item.strip()) for item in local_list]
        return return_list


def get_schedule(input_data):
    ''' Read buses' line into dict(position: bus) to keep position in list
    '''
    timestamp = int(input_data[0])
    schedule = dict()
    for position, bus in enumerate(input_data[1].split(',')):
        if (bus.isnumeric()):
            schedule[int(bus)] = position
    return (timestamp, schedule)


def get_next_bus(timestamp, schedule):
    ''' Return (next bus, delay) after given timestamp
    '''
    delta = 0
    while (delta < 10):
        for bus in schedule.keys():
            if (((timestamp+delta) % bus) == 0):
                return (bus, delta)
        delta += 1
    return (0, -1)


def check_timestamp(schedule, timestamp, offset=0):
    ''' Test for timestamp if a bus is coming
    '''
    for bus, delta in schedule.items():
        if (((timestamp+delta-offset) % bus) != 0):
            return False
    return True


def get_sweet_timespot_slow(schedule):
    ''' First try: Plain brute force for sweet timespot with given bus departure sequence
        Bad idea, useless
    '''
    timestamp = max(schedule.keys())
    check_max = len(schedule.keys())
    print(schedule, check_max)
    while (True):
        if (check_timestamp(schedule, timestamp)):
            return(timestamp)
        timestamp += 1
        if (timestamp % 1000000 == 0):
            print(timestamp//1000000, ' mio')
    return (0)


def get_sweet_timespot_timebased(schedule, timebase, offset=0):
    ''' Second try: less brute force for sweet timespot with given bus departure sequence
        Use bus numbers as iteration interval.
        Still useless...
    '''
    ticks = max(schedule.keys())
    while (True):
        if (check_timestamp(schedule, timebase*ticks, offset)):
            return(timebase*ticks)
        ticks += 1
    return (0)


def get_sweetspot_by_sieving(schedule):
    ''' Last try with internet inspiration: Use Chinese Remainder Sieving
        https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Search_by_sieving
        a_i = timestamp-position in list (delay i.e. modulo)
        n_i = bus numbers
        schedule: dict of {bus number: position}
    '''
    # according to reference: 0 <= a_i <= n_i:
    schedule = {bus: pos % bus for bus, pos in schedule.items()}
    bus_list = list(schedule.keys())
    bus_list.sort(reverse=True)
    timestamp = 0
    mult = 1
    print(timestamp, schedule)
    for idx in range(len(bus_list)-1):
        this_bus = bus_list[idx]
        next_bus = bus_list[idx+1]
        while ((timestamp + schedule[next_bus]) % next_bus != 0):
            timestamp += this_bus*mult
        mult *= this_bus
    return(timestamp)


def copycat(schedule):
    ''' Working algorithm from @jamhocken, adapted to local naming.
        Used as working reference to implement my sieving function
    '''
    bus_list = list(schedule.keys())
    ref_time = bus_list[0]
    print(ref_time, schedule)
    timestamp = 0
    for bus, pos in schedule.items():
        mult = 0
        while ((timestamp+ref_time*mult + pos) % bus != 0):
            mult += 1
        timestamp = timestamp + ref_time*mult
        if pos != 0:
            ref_time = ref_time*bus
    return timestamp


def main():
    daily_list = read_daily_input('input13.txt')
    timestamp, schedule = get_schedule(daily_list)
    bus, delta = get_next_bus(timestamp, schedule)
    print("Star1: ", bus*delta, "\n")

    print("Star2: ")
    print("- Copycatting: ", copycat(schedule))
    sweet_spot = get_sweetspot_by_sieving(schedule)
    print("- 'Own' chinese Sieving: ", sweet_spot)


if __name__ == "__main__":
    main()
