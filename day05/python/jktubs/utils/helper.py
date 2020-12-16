import re
import logging
import math
import sys

# By default the root logger is set to WARNING and all loggers you define
# inherit that value. Here we set the root logger to NOTSET. This logging
# level is automatically inherited by all existing and new sub-loggers
# that do not set a less verbose level.
logging.basicConfig(level=logging.NOTSET) #https://docs.python.org/3/library/logging.html#levels
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
#CRITICAL 50
#ERROR    40
#WARNING  30
#INFO     20
#DEBUG    10
#NOTSET    0
#log.info('info message')
#log.critical('critical message')
#log.debug('debug message')
#log.warning('warning message')
#log.error('error message')

def getVersion():
    log.debug("AoC2020_Day5!")


def read_file_to_list(filename):
    list = []
    file = open(filename, "r")
    for line in file:
        list.append(line)
    file.close()
    return list


# part 1
def get_seat_id(data):

    #m = re.search("^([FB]{7})([RL]{3})$", data)
    #log.debug("data: {}".format(data))
    #log.debug("match: {}".format(m))      # DEBUG:utils.helper:match: <re.Match object; span=(0, 10), match='BBFFBBFRLL'>
    #log.debug(type(m))                    # DEBUG:utils.helper:<class 're.Match'>

    exp = re.compile('^([FB]{7})([RL]{3})$')
    m = re.findall(exp, data)
    log.debug("match_list: {}".format(m)) #DEBUG:utils.helper:match_list: [('BBFFBBF', 'RLL')]
    log.debug(type(m))  # ==> list

    row_data  = m[0][0]
    seat_data = m[0][1]
    log.debug("row_data: {}, seat_data: {}".format(row_data, seat_data))

    upper = 127
    lower = 0
    n = 7
    for r in row_data:
        log.debug("r: {}".format(r))
        # F means to take the lower half
        if r == 'F':
            upper -= int(math.pow(2, n-1))
            log.debug("upper: {}, lower: {}".format(upper, lower))
        else: #B means to take the upper half
            lower += int(math.pow(2, n-1))
            log.debug("upper: {}, lower: {}".format(upper, lower))
        n -= 1

    if upper == lower:
        row = upper
        log.debug("row: {}".format(row))
    else:
        log.error("upper: {}, lower: {} do not match".format(upper, lower))
        sys.exit(-1)

    upper = 7
    lower = 0
    n = 3
    for c in seat_data:
        log.debug("c: {}".format(c))
        # L means to take the lower half
        if c == 'L':
            upper -= int(math.pow(2, n-1))
            log.debug("upper: {}, lower: {}".format(upper, lower))
        else: # R means to take the upper half
            lower += int(math.pow(2, n-1))
            log.debug("upper: {}, lower: {}".format(upper, lower))
        n -= 1

    if upper == lower:
        column = upper
        log.debug("column: {}".format(row))
    else:
        log.error("upper: {}, lower: {} do not match".format(upper, lower))
        sys.exit(-1)

    seat_id = row * 8 + column
    log.debug("row: {}, column: {}, seat_id: {}".format(row, column, seat_id))

    return seat_id
