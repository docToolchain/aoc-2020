# see README.doc

import copy
import time


def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [list(item.strip()) for item in local_list]
        return return_list


def create_dict(input_list):
    ''' Store initial configuration in dict.
        Returns {(coordinate tuple): status = 0 or 1}
        Returns limits of current pocket space
    '''
    z = 0
    w = 0
    pocket = dict()
    for line_nr, line in enumerate(input_list):
        for col_nr, status in enumerate(line):
            pocket[(z, col_nr, line_nr, w)] = 1 if (status == '#') else 0
    limits = ((0, 1), (0, col_nr+1), (0, line_nr+1), (0, 1))
    return pocket, limits


def get_adjacent(node, pocket):
    ''' Returns count of adjacent active nodes.
    '''
    count = 0
    nz = node[0]
    nx = node[1]
    ny = node[2]
    nw = node[3]
    adjacent_nodes = [(z, x, y, w)
                      for z in range(nz-1, nz+2) for x in range(nx-1, nx+2) for y in range(ny-1, ny+2) for w in range(nw-1, nw+2)]
    adjacent_nodes.remove(node)
    return sum([pocket[n] for n in adjacent_nodes if n in pocket.keys()])


def apply_rules(node_status, adjacent_count):
    ''' Returns status considering rules about node status and neighbor count
    '''
    if (adjacent_count == 3):
        return 1
    if ((node_status == 1) and (adjacent_count == 2)):
        return 1
    return 0


def iterate_pocket(pocket, limits, star):
    ''' Generate new iteration of pocket_status by checking rules
        Star = 1 -> 4th dimension w is kept fixed at 0
    '''
    new_pocket = dict()
    new_limits = list()
    for lim in limits:
        new_limits.append((lim[0] - 1, lim[1] + 1))
    z_lim = new_limits[0]
    x_lim = new_limits[1]
    y_lim = new_limits[2]
    w_lim = new_limits[3]
    for z in range(z_lim[0], z_lim[1]):
        for x in range(x_lim[0], x_lim[1]):
            for y in range(y_lim[0], y_lim[1]):
                if (star == 2):
                    for w in range(w_lim[0], w_lim[1]):
                        node = (z, x, y, w)
                        node_status = 0
                        if (node in pocket.keys()):
                            node_status = pocket[node]
                        new_pocket[node] = apply_rules(
                            node_status, get_adjacent(node, pocket))
                else:
                    w = 0
                    node = (z, x, y, w)
                    node_status = 0
                    if (node in pocket.keys()):
                        node_status = pocket[node]
                    new_pocket[node] = apply_rules(
                        node_status, get_adjacent(node, pocket))
    return new_pocket, new_limits


def show_layer(z, pocket, limits):
    ''' Display single layer z status (in w==0 projection)
    '''
    w = 0
    for line_nr in range(*limits[2]):
        line = "".join([str(pocket[(z, x, line_nr, w)])
                        for x in range(*limits[1])])
        print(z, " - ", line)


def boot_pocket(pocket, limits, iterations, star=2):
    ''' Iterates pocket for given number of iterations.
        Returns number of active nodes
    '''
    show_layer(0, pocket, limits)
    for cycle in range(iterations):
        pocket, limits = iterate_pocket(pocket, limits, star)
        print("Iteration: ", cycle)
        show_layer(0, pocket, limits)
    return sum(pocket.values())


def main():
    daily_list = read_daily_input('input17.txt')
    pocket, limits = create_dict(daily_list)
    star1 = boot_pocket(pocket, limits, 6, star=1)
    print(f"Active cubes: {star1}")
    star2 = boot_pocket(pocket, limits, 6, star=2)
    print(f"Active cubes: {star1}")
    print(f"Hyperactive cubes: {star2}")


if __name__ == "__main__":
    main()
