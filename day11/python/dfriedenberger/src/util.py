

# tag::Map[]
class SeatMap():

    def loadFromFile(self, filename):
        """Read file to map"""
        self._rows = []
        self.width = 0
        file = open(filename, "r")
        for line in file:
            self._rows.append(line.strip())
            self.width = max(self.width,len(line.strip()))
        self.height = len(self._rows)
        file.close()


    def get(self,x,y):
        return self._rows[y][x]

    def occupied(self,x,y):
        o = 0
        for i in range(x-1,x+2):
            if i < 0: continue
            if i >= self.width: continue
                        
            for j in range(y-1,y+2):
                if j < 0: continue
                if j >= self.height: continue
                if x == i and y == j: continue
                if self.get(i,j) == '#':
                    o += 1
        return o
    def occupied2line(self,x0,y0,xoff,yoff):
        x = x0 + xoff
        y = y0 + yoff
        if x < 0: return 0
        if x >= self.width: return 0
        if y < 0: return 0
        if y >= self.height: return 0

        t = self.get(x,y)
        if t == '.': return self.occupied2line(x,y,xoff,yoff)
        if t == 'L': return 0
        return 1

    def occupied2(self,x,y):
        o = 0
        o += self.occupied2line(x,y,-1,-1)
        o += self.occupied2line(x,y,0,-1)
        o += self.occupied2line(x,y,1,-1)
        o += self.occupied2line(x,y,-1,0)
        o += self.occupied2line(x,y,1,0)
        o += self.occupied2line(x,y,-1,1)
        o += self.occupied2line(x,y,0,1)
        o += self.occupied2line(x,y,1,1)
        return o

    def next(self):
        next = []
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                o = self.occupied(x,y)
                t = self.get(x,y)
                if t == 'L' and o == 0:
                    t = '#'
                if t == '#' and o >= 4:
                    t = 'L'
                line += t;
            next.append(line)
        nextMap = SeatMap()
        nextMap._rows = next
        nextMap.width = len(next[0])
        nextMap.height = len(next)

        return nextMap

    def next2(self):
            next = []
            for y in range(self.height):
                line = ""
                for x in range(self.width):
                    o = self.occupied2(x,y)
                    t = self.get(x,y)
                    if t == 'L' and o == 0:
                        t = '#'
                    if t == '#' and o >= 5:
                        t = 'L'
                    line += t;
                next.append(line)
            nextMap = SeatMap()
            nextMap._rows = next
            nextMap.width = len(next[0])
            nextMap.height = len(next)

            return nextMap


    def equals(self,map):
        for x in range(self.width):
            for y in range(self.height):
                if self.get(x,y) != map.get(x,y):
                    return False
        return True

    def count(self):
        o = 0
        for x in range(self.width):
            for y in range(self.height):
                if self.get(x,y) == '#':
                    o += 1
        return o

    def dump(self):
        for row in self._rows:
            print(row)
        return
# tag::Map[]
