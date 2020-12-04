

# tag::countTrees[]
def count_trees(treeMap,xsteps,ysteps):
    x = 0
    y = 0
    trees = 0
    while(y < treeMap.height):
        c = treeMap.get(x,y)
        if(c == '#'):
            trees = trees + 1;
        x = (x + xsteps) %  treeMap.width
        y = y + ysteps
    return trees
# end::countTrees[]

# tag::TreeMap[]
class TreeMap():

    def __init__(self, filename):
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

    def dump(self):
        print(self._rows)
        return
# tag::TreeMap[]
