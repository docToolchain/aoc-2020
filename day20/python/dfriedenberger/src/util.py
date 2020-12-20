import re
import math
import copy


def read_file_to_list(filename):
        """Read file to map"""
        tiles = []
        
        file = open(filename, "r")
        for line in file:
            line = line.strip()
            if line == "": continue

            #Tile
            m = re.search(r'^Tile\s+([0-9]+):$', line)
            if m: 
                tile = Tile(int(m.group(1)))
                tiles.append(tile)
                continue

            m = re.search(r'^([.#]+)$', line)
            if m: 
                tile.appendRow(m.group(1))
                continue
            raise Exception(line)
        return tiles


# tag::backtracking[]

def find_solution(tiles,rows,used,x,y):

    #print(rows)
    #test 
    if len(tiles) == len(used):
        return rows

    if y >= len(rows):
        rows.append([])

    for tile in tiles:
        if tile.id in used: continue
        nused = copy.deepcopy(used)
        nused.add(tile.id)
        #try 2 flips and 4 rotations
        for vtile in tile.getVariants():
           #test top
           if y > 0:
               if vtile.pattern["top"] != rows[y-1][x].pattern["bottom"]: continue
           #test left
           if x > 0:
               if vtile.pattern["left"] != rows[y][x-1].pattern["right"]: continue

           # vtiles matches
           nrows = copy.deepcopy(rows)
           nrows[y].append(vtile)
           
           if len(nrows[y]) < math.sqrt(len(tiles)):
               #test right
               s = find_solution(tiles,nrows,nused,x+1,y)
               if s: return s
           else: 
               #test next line
               s =  find_solution(tiles,nrows,nused,0,y+1)
               if s: return s

    return None
# end::backtracking[]

def concat_Tiles(solution):
    map = Tile(0)
    for tiles in solution:
        for y in range(1,len(tiles[0].rows)-1):
            line = ""
            for tile in tiles:
                for x in range(1,len(tile.rows[y])-1):
                    line += tile.rows[y][x]
            map.appendRow(line)
    return map

def match_pattern(map,monster,x0,y0):
    for y in range(len(monster)):
        for x in range(len(monster[0])):
            if monster[y][x] != "#": continue #optimize
            if map.get(x0 + x,y0 + y) != "#": return False
    return True

def find_pattern(map,monster):
    result = []
    for y in range(len(map.rows)):
        for x in range(len(map.rows[0])):
            if match_pattern(map,monster,x,y):
                result.append((x,y))
    return result

# tag::Tile[]
class Tile():

    def __init__(self,id):
        """Read file to map"""
        self.id = id
        self.rows = []
        self.pattern = { "left" : "" , "right": "" , "top": None , "bottom": None }
        self.left = ""

    def __repr__(self):
        return str(self.id)

    def appendRow(self,row):
        if len(self.rows) == 0:
            self.pattern["top"] = row
        self.pattern["left"] += row[0]
        self.pattern["right"] += row[-1]
        self.pattern["bottom"] = row
        self.rows.append(row)

    def flip(self):
        tile = Tile(self.id)
        for row in self.rows:
            tile.appendRow(row[::-1])
        return tile

    def rotate(self):
        tile = Tile(self.id)
        l = len(self.rows)
        for y in range(l):
            row = ""
            for x in range(l):
                row += self.rows[x][l-y-1]
            tile.appendRow(row);
        return tile

    def get(self,x,y):
        if y >= len(self.rows): return None
        if x >= len(self.rows[0]): return None
        return self.rows[y][x]

    def count(self):
        c = 0
        for row in self.rows:
             c += row.count('#')
        return c

    def dump(self):
        print("Tile",self.id)
        for row in self.rows:
            print(row)
    
    def createVariants(self):
        self.variants = []
        tile = self 
        for i in range(2):
            for j in range(4): #for 4 rotation
                self.variants.append(tile)
                tile = tile.rotate()
            tile = tile.flip()

    def getVariants(self):
        return self.variants

# tag::Tile[]
