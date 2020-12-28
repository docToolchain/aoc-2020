from pathlib import Path

#tag::test_example[]
example_input = """.#.
..#
###
"""

def create_life(world, input_data, life):
    world.read_state(input_data)
    l = life(world)
    l.execute_cycle(6)
    return l.world.active_count()

def test_example():
    assert create_life(SimpleWorld(), example_input, SimpleLife) == 112
#end::test_example[]

#def::example[]
class SimpleWorld:
    def __init__(self):
        self.clear()

    def clear(self):
        self.active = set()
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.min_z = 0
        self.max_z = 0

    def read_state(self, cell_data):
        self.clear()
        for y,line in enumerate(cell_data.splitlines()):
            for x,cell in enumerate(line):
                if cell == "#":
                    self.activate(x, y, 0)

    def activate(self, x, y, z):
        self.active.add((x,y,z))
        if x >= self.max_x:
            self.max_x = x
        if x <= self.min_x:
            self.min_x = x
        if y >= self.max_y:
            self.max_y = y
        if y <= self.min_y:
            self.min_y = y
        if z >= self.max_z:
            self.max_z = z
        if z <= self.min_z:
            self.min_z = z

    def active_count(self):
        return len(self.active)

class SimpleLife:
    def __init__(self, world):
        self.world = world

    def execute_cycle(self, count=1):
        for _ in range(count):
            new_world = SimpleWorld()
            for x in range(self.world.min_x-1, self.world.max_x+2):
                for y in range(self.world.min_y-1, self.world.max_y+2):
                    for z in range(self.world.min_z-1, self.world.max_z+2):
                        neighbors = 0
                        for dx in range(-1,2):
                            for dy in range(-1,2):
                                for dz in range(-1,2):
                                    if dx != 0 or dy != 0 or dz != 0:
                                        if (x+dx, y+dy, z+dz) in self.world.active:
                                            neighbors += 1
                        if (x,y,z) in self.world.active:
                            if neighbors == 2 or neighbors == 3:
                                new_world.activate(x,y,z)
                        else:
                            if neighbors == 3:
                                new_world.activate(x,y,z)
            self.world = new_world
#end::example[]

#def::star1[]
def read_input():
    with Path("input.txt").open() as f:
        return f.read()

def test_answer1():
    assert create_life(SimpleWorld(), read_input(), SimpleLife) == 336
#end::star1[]

#def::test_recursive_example[]
def test_recursive_example():
    assert create_life(MultiWorld(3), example_input, RecursiveLife) == 112
    assert create_life(MultiWorld(4), example_input, RecursiveLife) == 848
#end::test_recursive_example[]

#def::recursive_example[]
class MultiWorld:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.clear()

    def clear(self):
        self.active = set()
        for i in range(self.dimensions):
            self.min = [None] * self.dimensions
            self.max = [None] * self.dimensions

    def read_state(self, cell_data):
        self.clear()
        for y,line in enumerate(cell_data.splitlines()):
            for x,cell in enumerate(line):
                if cell == "#":
                    cell_coordinates = [x,y]
                    for i in range(2,self.dimensions):
                        cell_coordinates.append(0)
                    self.activate(cell_coordinates)

    def activate(self, cell):
        if not tuple(cell) in self.active:
            self.active.add(tuple(cell))
            for i in range(self.dimensions):
                if self.max[i] == None or cell[i] > self.max[i]:
                    self.max[i] = cell[i]
                if self.min[i] == None or cell[i] < self.min[i]:
                    self.min[i] = cell[i]

    def deactivate(self, cell):
        self.active.remove(tuple(cell))

    def is_active(self, cell):
        return tuple(cell) in self.active

    def range_for_dimension(self, d):
        return range(self.min[d], self.max[d]+1)

    def range_for_dimension_plus(self, d):
        return range(self.min[d]-1, self.max[d]+2)

    def active_count(self):
        return len(self.active)

class RecursiveLife:
    def __init__(self, world):
        self.world = world
        self.survival = [2,3]
        self.birth = [3]

    def count_neighbor(self, cell, delta):
        for i in range(len(delta)):
            if delta[i] != 0:
                neighbor = [0] * len(cell)
                for j in range(len(cell)):
                    neighbor[j] = cell[j] + delta[j]
                if self.world.is_active(neighbor):
                    return 1
                else:
                    return 0
        return 0

    def count_all_neighbors(self, cell, delta, dimension):
        if dimension == 0:
            return self.count_neighbor(cell, delta)

        neighbors = 0
        for d in range(-1,2):
            neighbors += self.count_all_neighbors(cell, delta + [d], dimension - 1)
        return neighbors

    def check_cell(self, new_world, cell):
        neighbors = self.count_all_neighbors(cell, [], self.world.dimensions)
        if self.world.is_active(cell):
            if neighbors in self.survival:
                new_world.activate(cell)
        else:
            if neighbors in self.birth:
                new_world.activate(cell)

    def check_all_cells(self, new_world, cell, dimension):
        if dimension == self.world.dimensions:
            self.check_cell(new_world, cell)
            return

        for i in self.world.range_for_dimension_plus(dimension):
            self.check_all_cells(new_world, cell + [i], dimension + 1)

    def execute_cycle(self, count=1):
        for _ in range(count):
            new_world = MultiWorld(self.world.dimensions)
            self.check_all_cells(new_world, [], 0)
            self.world = new_world
#end::recursive_example[]

#def::star2[]
def test_star2():
    assert create_life(MultiWorld(4), read_input(), RecursiveLife) == 2620
#end::star2[]
