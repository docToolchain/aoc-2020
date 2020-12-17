import re

# tag::Cube[]
class Cube():

    def __init__(self):
        self.cubes = dict()

    def loadFromFile(self, filename):
        """Read file to map"""
        file = open(filename, "r")
        z = 0
        y = 0
        for line in file:
            for x in range(len(line.strip())):
                if line[x] == '#':
                    self.set(x,y,z)
            y += 1                    
        file.close()

    def set(self,x,y,z):
        key = "{0}#{1}#{2}".format(x,y,z)   
        self.cubes[key] = "#"

    def get(self,x,y,z):
        key = "{0}#{1}#{2}".format(x,y,z)
        if key not in self.cubes: return '.'
        return self.cubes[key]

    def getLoopRange(self):
        x1,x2,y1,y2,z1,z2 = 0,1,0,1,0,1
        for key in self.cubes:
            m = re.search(r'^([0-9-]+)#([0-9-]+)#([0-9-]+)$', key)
            if not m: raise Exception(key)
            x = int(m.group(1))
            x1,x2 = min(x1,x) , max(x2,x + 1)
            y = int(m.group(2))
            y1,y2 = min(y1,y) , max(y2,y + 1)
            z = int(m.group(3))
            z1,z2 = min(z1,z) , max(z2,z + 1)
        return x1,x2,y1,y2,z1,z2

    def getActiveNeighbors(self,x,y,z):
        o = 0
        for z0 in range(z-1,z+2):
            for y0 in range(y-1,y+2):
                for x0 in range(x-1,x+2):
                    if x0 == x and y0 == y and z0 == z: continue
                    if self.get(x0,y0,z0) == "#": o += 1
        return o

    def next(self):
        next = Cube()
        x1,x2,y1,y2,z1,z2 = self.getLoopRange()

        for z in range(z1-1,z2+1):
            for y in range(y1-1,y2+1):
                for x in range(x1-1,x2+1):
                    o = self.getActiveNeighbors(x,y,z)
                    if self.get(x,y,z) == "#":
                        #active and exactly 2 or 3 of its neighbors are also active, the cube remains active
                        if o == 2 or o == 3:
                            next.set(x,y,z)
                    else:
                        #If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active
                        if o == 3:
                            next.set(x,y,z)
      
        return next


    def count(self):
        return len(self.cubes)

    def dump(self):

        x1,x2,y1,y2,z1,z2 = self.getLoopRange()
        print("---",x1,x2,y1,y2,z1,z2)
        for z in range(z1,z2):
            print("z =",z);
            for y in range(y1,y2):
                row = "";
                for x in range(x1,x2):
                    row += self.get(x,y,z)
                print(row)
        return
# tag::Cube[]

# tag::Cube4D[]
class Cube4D():

    def __init__(self):
        self.cubes = dict()

    def loadFromFile(self, filename):
        """Read file to map"""
        file = open(filename, "r")
        z = 0
        w = 0
        y = 0
        for line in file:
            for x in range(len(line.strip())):
                if line[x] == '#':
                    self.set(x,y,z,w)
            y += 1                    
        file.close()

    def set(self,x,y,z,w):
        key = "{0}#{1}#{2}#{3}".format(x,y,z,w)   
        self.cubes[key] = "#"

    def get(self,x,y,z,w):
        key = "{0}#{1}#{2}#{3}".format(x,y,z,w)
        if key not in self.cubes: return '.'
        return self.cubes[key]

    def getLoopRange(self):
        x1,x2,y1,y2,z1,z2,w1,w2 = 0,1,0,1,0,1,0,1
        for key in self.cubes:
            m = re.search(r'^([0-9-]+)#([0-9-]+)#([0-9-]+)#([0-9-]+)$', key)
            if not m: raise Exception(key)
            x = int(m.group(1))
            x1,x2 = min(x1,x) , max(x2,x + 1)
            y = int(m.group(2))
            y1,y2 = min(y1,y) , max(y2,y + 1)
            z = int(m.group(3))
            z1,z2 = min(z1,z) , max(z2,z + 1)
            w = int(m.group(4))
            w1,w2 = min(w1,w) , max(w2,w + 1)
        return x1,x2,y1,y2,z1,z2,w1,w2

    def getActiveNeighbors(self,x,y,z,w):
        o = 0
        for w0 in range(w-1,w+2):
            for z0 in range(z-1,z+2):
                for y0 in range(y-1,y+2):
                    for x0 in range(x-1,x+2):
                        if x0 == x and y0 == y and z0 == z and w0 == w: continue
                        if self.get(x0,y0,z0,w0) == "#": o += 1
        return o

    def next(self):
        next = Cube4D()
        x1,x2,y1,y2,z1,z2,w1,w2 = self.getLoopRange()

        for w in range(w1-1,w2+1):
            for z in range(z1-1,z2+1):
                for y in range(y1-1,y2+1):
                    for x in range(x1-1,x2+1):
                        o = self.getActiveNeighbors(x,y,z,w)
                        if self.get(x,y,z,w) == "#":
                            #active and exactly 2 or 3 of its neighbors are also active, the cube remains active
                            if o == 2 or o == 3:
                                next.set(x,y,z,w)
                        else:
                            #If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active
                            if o == 3:
                                next.set(x,y,z,w)
        
        return next


    def count(self):
        return len(self.cubes)

    def dump(self):

        x1,x2,y1,y2,z1,z2,w1,w2 = self.getLoopRange()
        for w in range(w1,w2):
            for z in range(z1,z2):
                print("z =",z,"w =",w);
                for y in range(y1,y2):
                    row = "";
                    for x in range(x1,x2):
                        row += self.get(x,y,z,w)
                    print(row)
        return
# tag::Cube4D[]