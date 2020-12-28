from pathlib import Path

#tag::test_example[]
example_input = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
"""

def test_example():
    world = World(2)
    world.read_tiles(example_input)
    assert world.active_count() == 10
#end::test_example[]

#tag::example[]
class World:
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

    def find_tile(self, path):
        x = 0
        y = 0

        i = 0
        while i < len(path):
            if path[i] == "w":
                x -= 1
                i += 1
            elif path[i] == "e":
                x += 1
                i += 1
            elif path[i] == "n":
                y += 1
                if path[i+1] == "w":
                    x -= 1
                i += 2
            elif path[i] == "s":
                y -= 1
                if path[i+1] == "e":
                    x += 1
                i += 2
        return [x,y]

    def read_tiles(self, input_data):
        for line in input_data.splitlines():
            if line:
                pos = self.find_tile(line)
                if self.is_active(pos):
                    self.deactivate(pos)
                else:
                    self.activate(pos)

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
#end::example[]

#tag::star1[]
def read_input():
    with Path("input.txt").open() as f:
        return f.read()

def test_star1():
    world = World(2)
    world.read_tiles(read_input())
    assert world.active_count() == 330
#end::star1[]

#tag::test_hex_example[]
example_input_day17 = """.#.
..#
###
"""

def create_life(world, input_data, life):
    world.read_state(input_data)
    l = life(world)
    l.execute_cycle(6)
    return l.world.active_count()

def create_hex_life(input_data):
    world = World(2)
    world.read_tiles(input_data)
    life = Life(world)
    life.survival = [1,2]
    life.birth = [2]
    life.hexagons = True
    return life

def test_hex_example():
    assert create_life(World(3), example_input_day17, Life) == 112
    assert create_life(World(4), example_input_day17, Life) == 848

    l = create_hex_life(example_input)
    l.execute_cycle()
    assert l.world.active_count() == 15
    l.execute_cycle()
    assert l.world.active_count() == 12
    l.execute_cycle(98)
    assert l.world.active_count() == 2208
#end::test_hex_example[]

#tag::hex_example[]
class Life:
    def __init__(self, world):
        self.world = world
        self.survival = [2,3]
        self.birth = [3]
        self.hexagons = False

    def count_neighbor(self, cell, delta):
        for i in range(len(delta)):
            if delta[i] != 0:
                neighbor = [0] * len(cell)
                for j in range(len(cell)):
                    neighbor[j] = cell[j] + delta[j]
                if self.world.is_active(neighbor):
                    if self.hexagons and delta[0] == 1 and delta[1] == 1:
                        return 0
                    if self.hexagons and delta[0] == -1 and delta[1] == -1:
                        return 0
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
            new_world = World(self.world.dimensions)
            self.check_all_cells(new_world, [], 0)
            self.world = new_world
#end::hex_example[]

#def::star2[]
def test_star2():
    life = create_hex_life(read_input())
    life.execute_cycle(100)
    assert life.world.active_count() == 3711
#end::star2[]
