import org.apache.commons.lang3.StringUtils

// testPart1()
// testPart2()
solve()

void solve() {
    // tag::splitInput[]
    ArrayList<ArrayList> inputPart1 = getStartObjectPart1("input.txt")
    println("Solution Part 1: " + solvePart1(inputPart1, 6))
    ArrayList<ArrayList> inputPart2 = getStartObjectPart2("input.txt")
    println("Solution Part 2: " + solvePart2(inputPart2, 6))
    // end::splitInput[]
}

int solvePart1(ArrayList<ArrayList> grid, int cycles) {
    // tag::solvePart1[]
    for(int i = 0; i < cycles; i++) {
        grid = doCyclePart1(grid)
    }
    return countActiveCubesPart1(grid)
    // end::solvePart1[]
}

ArrayList getStartObjectPart1(String input){
    ArrayList<ArrayList> inputList = Arrays.asList(new File(input).text.split(System.getProperty("line.separator"))).collect {
        Arrays.asList(it.split("")) as ArrayList<String>
    }
    ArrayList<ArrayList> startObject = new ArrayList<>()
    startObject.add(inputList)
    return startObject
}

ArrayList extendGridPart1(ArrayList grid) {
    grid = deepcopy(grid)
    grid = extendGridXPart1(grid)
    grid = extendGridYPart1(grid)
    grid = extendGridZPart1(grid)

    return grid
}

ArrayList extendGridXPart1(ArrayList grid) {
    grid.forEach{ ArrayList slice ->
        slice.forEach{ ArrayList row ->
            row.add(0, ".")
            row.add(".")
        }
    }
    return grid
}

ArrayList extendGridYPart1(ArrayList grid) {
    int xSize = ((grid.get(0) as ArrayList).get(0) as ArrayList).size()
    grid.forEach{ ArrayList slice ->
        slice.add(0, getNewRow(xSize))
        slice.add(getNewRow(xSize))
    }
    return grid
}

ArrayList extendGridZPart1(ArrayList grid) {
    int xSize = ((grid.get(0) as ArrayList).get(0) as ArrayList).size()
    int ySize = (grid.get(0) as ArrayList).size()
    grid.add(0, getNewSlice(xSize, ySize))
    grid.add(getNewSlice(xSize, ySize))
    return grid
}

ArrayList getNewRow(int xSize) {
    return Arrays.asList(StringUtils.repeat(".", xSize).split("")) as ArrayList
}

ArrayList getNewSlice(int xSize, int ySize) {
    ArrayList<ArrayList> slice = new ArrayList()
    for(int i = 0; i < ySize; i++) {
        slice.add(getNewRow(xSize))
    }
    return slice
}

ArrayList getNewCube(int xSize, int ySize, int zSize) {
    ArrayList<ArrayList> cube = new ArrayList()
    for(int i = 0; i < zSize; i++) {
        cube.add(getNewSlice(xSize, ySize))
    }
    return cube
}

int getNeighboursPart1(ArrayList grid, int posX, int posY, int posZ) {
    int neighbours = 0
    int xSize = ((grid.get(0) as ArrayList).get(0) as ArrayList).size()
    int ySize = (grid.get(0) as ArrayList).size()
    int zSize = grid.size()
    int xFrom = posX==0 ? 0 : posX-1
    int xTo = posX == xSize-1 ? xSize-1 : posX+1
    for(int x = xFrom; x <= xTo; x++) {
        int yFrom = posY==0 ? 0 : posY-1
        int yTo = posY == ySize-1 ? ySize-1 : posY+1
        for(int y = yFrom; y <= yTo; y++) {
            int zFrom = posZ==0 ? 0 : posZ-1
            int zTo = posZ == zSize-1 ? zSize-1 : posZ+1
            for(int z = zFrom; z <= zTo; z++) {
                if(!(x == posX && y == posY && z == posZ)) {
                    neighbours += ((grid.get(z) as ArrayList).get(y) as ArrayList).get(x) == "#" ? 1 : 0
                }
            }
        }
    }
    return neighbours
}

ArrayList doCyclePart1(ArrayList grid) {
    grid = extendGridPart1(grid)
    ArrayList newGrid = deepcopy(grid) as ArrayList
    int xSize = ((grid.get(0) as ArrayList).get(0) as ArrayList).size()
    int ySize = (grid.get(0) as ArrayList).size()
    int zSize = grid.size()
    for(int x = 0; x < xSize; x++) {
        for(int y = 0; y < ySize; y++) {
            for(int z = 0; z < zSize; z++) {
                String cube = ((grid.get(z) as ArrayList).get(y) as ArrayList).get(x)
                int neighbours = getNeighboursPart1(grid, x, y, z)
                if(cube == "#") {
                    if(neighbours == 2 || neighbours == 3) {
                        ((newGrid.get(z) as ArrayList).get(y) as ArrayList).set(x, "#")
                    } else {
                        ((newGrid.get(z) as ArrayList).get(y) as ArrayList).set(x, ".")
                    }
                } else {
                    if(neighbours == 3) {
                        ((newGrid.get(z) as ArrayList).get(y) as ArrayList).set(x, "#")
                    } else {
                        ((newGrid.get(z) as ArrayList).get(y) as ArrayList).set(x, ".")
                    }
                }
            }
        }
    }
    return newGrid
}

int countActiveCubesPart1(ArrayList grid) {
    int activeCubes = 0
    int xSize = ((grid.get(0) as ArrayList).get(0) as ArrayList).size()
    int ySize = (grid.get(0) as ArrayList).size()
    int zSize = grid.size()
    for(int x = 0; x < xSize; x++) {
        for(int y = 0; y < ySize; y++) {
            for(int z = 0; z < zSize; z++) {
                activeCubes += ((grid.get(z) as ArrayList).get(y) as ArrayList).get(x) == "#" ? 1 : 0
            }
        }
    }
    return activeCubes
}

void testPart1() {
    ArrayList<ArrayList> input = getStartObjectPart1("input_test_1.txt")
    ArrayList cicle1 = doCyclePart1(input)
    println("0 Cycles:")
    printGridPart1(input)
    println("1 Cycle:")
    printGridPart1(cicle1)

    int neighbours
    neighbours = getNeighboursPart1(input, 0, 0, 0)
    assert neighbours == 1
    neighbours = getNeighboursPart1(input, 1, 1, 0)
    assert neighbours == 5

    assert countActiveCubesPart1(input) == 5
    assert countActiveCubesPart1(cicle1) == 11

    assert solvePart1(input, 6) == 112
}

int solvePart2(ArrayList<ArrayList> grid, int cycles) {
    // tag::solvePart2[]
    for(int i = 0; i < cycles; i++) {
        grid = doCyclePart2(grid)
    }
    return countActiveCubesPart2(grid)
    // end::solvePart2[]
}

ArrayList getStartObjectPart2(String input){
    ArrayList<ArrayList> inputList = Arrays.asList(new File(input).text.split(System.getProperty("line.separator"))).collect {
        Arrays.asList(it.split("")) as ArrayList<String>
    }
    ArrayList<ArrayList> startObject = new ArrayList<>()
    startObject.add(inputList)
    ArrayList<ArrayList> fourthDim = new ArrayList<>()
    fourthDim.add(startObject)
    return fourthDim
}

ArrayList extendGridPart2(ArrayList grid) {
    grid = deepcopy(grid) as ArrayList
    grid = extendGridXPart2(grid)
    grid = extendGridYPart2(grid)
    grid = extendGridZPart2(grid)
    grid = extendGridWPart2(grid)

    return grid
}

ArrayList extendGridXPart2(ArrayList grid) {
    grid.forEach{ ArrayList cube ->
        cube.forEach { ArrayList slice ->
            slice.forEach { ArrayList row ->
                row.add(0, ".")
                row.add(".")
            }
        }
    }
    return grid
}

ArrayList extendGridYPart2(ArrayList grid) {
    int xSize = (((grid.get(0) as ArrayList).get(0) as ArrayList).get(0) as ArrayList).size()
    grid.forEach{ ArrayList cube ->
        cube.forEach { ArrayList slice ->
            slice.add(0, getNewRow(xSize))
            slice.add(getNewRow(xSize))
        }
    }
    return grid
}

ArrayList extendGridZPart2(ArrayList grid) {
    int xSize = (((grid.get(0) as ArrayList).get(0) as ArrayList).get(0) as ArrayList).size()
    int ySize = ((grid.get(0) as ArrayList).get(0) as ArrayList).size()
    grid.forEach { ArrayList cube ->
        cube.add(0, getNewSlice(xSize, ySize))
        cube.add(getNewSlice(xSize, ySize))
    }
    return grid
}

ArrayList extendGridWPart2(ArrayList grid) {
    int xSize = (((grid.get(0) as ArrayList).get(0) as ArrayList).get(0) as ArrayList).size()
    int ySize = ((grid.get(0) as ArrayList).get(0) as ArrayList).size()
    int zSize = (grid.get(0) as ArrayList).size()
    grid.add(0, getNewCube(xSize, ySize, zSize))
    grid.add(getNewCube(xSize, ySize, zSize))
    return grid
}

int getNeighboursPart2(ArrayList grid, int posX, int posY, int posZ, int posW) {
    int neighbours = 0
    int xSize = (((grid.get(0) as ArrayList).get(0) as ArrayList).get(0) as ArrayList).size()
    int ySize = ((grid.get(0) as ArrayList).get(0) as ArrayList).size()
    int zSize = (grid.get(0) as ArrayList).size()
    int wSize = grid.size()
    int xFrom = posX==0 ? 0 : posX-1
    int xTo = posX == xSize-1 ? xSize-1 : posX+1
    for(int x = xFrom; x <= xTo; x++) {
        int yFrom = posY==0 ? 0 : posY-1
        int yTo = posY == ySize-1 ? ySize-1 : posY+1
        for(int y = yFrom; y <= yTo; y++) {
            int zFrom = posZ==0 ? 0 : posZ-1
            int zTo = posZ == zSize-1 ? zSize-1 : posZ+1
            for(int z = zFrom; z <= zTo; z++) {
                int wFrom = posW==0 ? 0 : posW-1
                int wTo = posW == wSize-1 ? wSize-1 : posW+1
                for(int w = wFrom; w <= wTo; w++) {
                    if (!(x == posX && y == posY && z == posZ && w == posW)) {
                        neighbours += (((grid.get(w) as ArrayList).get(z) as ArrayList).get(y) as ArrayList).get(x) == "#" ? 1 : 0
                    }
                }
            }
        }
    }
    return neighbours
}

ArrayList doCyclePart2(ArrayList grid) {
    grid = extendGridPart2(grid)
    ArrayList newGrid = deepcopy(grid) as ArrayList
    int xSize = (((grid.get(0) as ArrayList).get(0) as ArrayList).get(0) as ArrayList).size()
    int ySize = ((grid.get(0) as ArrayList).get(0) as ArrayList).size()
    int zSize = (grid.get(0) as ArrayList).size()
    int wSize = grid.size()
    for(int x = 0; x < xSize; x++) {
        for(int y = 0; y < ySize; y++) {
            for(int z = 0; z < zSize; z++) {
                for(int w = 0; w < wSize; w++) {
                    String cube = (((grid.get(w) as ArrayList).get(z) as ArrayList).get(y) as ArrayList).get(x)
                    int neighbours = getNeighboursPart2(grid, x, y, z, w)
                    if (cube == "#") {
                        if (neighbours == 2 || neighbours == 3) {
                            (((newGrid.get(w) as ArrayList).get(z) as ArrayList).get(y) as ArrayList).set(x, "#")
                        } else {
                            (((newGrid.get(w) as ArrayList).get(z) as ArrayList).get(y) as ArrayList).set(x, ".")
                        }
                    } else {
                        if (neighbours == 3) {
                            (((newGrid.get(w) as ArrayList).get(z) as ArrayList).get(y) as ArrayList).set(x, "#")
                        } else {
                            (((newGrid.get(w) as ArrayList).get(z) as ArrayList).get(y) as ArrayList).set(x, ".")
                        }
                    }
                }
            }
        }
    }
    return newGrid
}

int countActiveCubesPart2(ArrayList grid) {
    int activeCubes = 0
    int xSize = (((grid.get(0) as ArrayList).get(0) as ArrayList).get(0) as ArrayList).size()
    int ySize = ((grid.get(0) as ArrayList).get(0) as ArrayList).size()
    int zSize = (grid.get(0) as ArrayList).size()
    int wSize = grid.size()
    for(int x = 0; x < xSize; x++) {
        for(int y = 0; y < ySize; y++) {
            for(int z = 0; z < zSize; z++) {
                for(int w = 0; w < wSize; w++) {
                    activeCubes += (((grid.get(w) as ArrayList).get(z) as ArrayList).get(y) as ArrayList).get(x) == "#" ? 1 : 0
                }
            }
        }
    }
    return activeCubes
}

void testPart2() {
    ArrayList<ArrayList> input = getStartObjectPart2("input_test_1.txt")
    ArrayList cicle1 = doCyclePart2(input)
    println("0 Cycles:")
    printGridPart2(input)
    println("1 Cycle:")
    printGridPart2(cicle1)

    int neighbours
    neighbours = getNeighboursPart2(input, 0, 0, 0, 0)
    assert neighbours == 1
    neighbours = getNeighboursPart2(input, 1, 1, 0, 0)
    assert neighbours == 5

    assert countActiveCubesPart2(input) == 5
    assert countActiveCubesPart2(cicle1) == 29

    assert solvePart2(input, 6) == 848
}

void printGridPart1(ArrayList grid) {
    int xSize = ((grid.get(0) as ArrayList).get(0) as ArrayList).size()
    int ySize = (grid.get(0) as ArrayList).size()
    int zSize = grid.size()
    for(int z = 0; z < zSize; z++) {
        for(int y = 0; y < ySize; y++) {
            for(int x = 0; x < xSize; x++) {
                print(((grid.get(z) as ArrayList).get(y) as ArrayList).get(x))
            }
            print(System.lineSeparator())
        }
        print(System.lineSeparator())
    }
}

void printGridPart2(ArrayList grid) {
    int xSize = (((grid.get(0) as ArrayList).get(0) as ArrayList).get(0) as ArrayList).size()
    int ySize = ((grid.get(0) as ArrayList).get(0) as ArrayList).size()
    int zSize = (grid.get(0) as ArrayList).size()
    int wSize = grid.size()
    for(int w = 0; w < wSize; w++) {
        for(int z = 0; z < zSize; z++) {
            for(int y = 0; y < ySize; y++) {
                for(int x = 0; x < xSize; x++) {
                    print((((grid.get(w) as ArrayList).get(z) as ArrayList).get(y) as ArrayList).get(x))
                }
                print(System.lineSeparator())
            }
            print(System.lineSeparator())
        }
        print(System.lineSeparator())
    }
}

// standard deep copy implementation
def deepcopy(orig) {
    bos = new ByteArrayOutputStream()
    oos = new ObjectOutputStream(bos)
    oos.writeObject(orig); oos.flush()
    bin = new ByteArrayInputStream(bos.toByteArray())
    ois = new ObjectInputStream(bin)
    return ois.readObject()
}
