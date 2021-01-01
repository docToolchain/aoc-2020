testPart1()
testPart2()
solve()

static void solve() {
    // tag::splitInput[]
    ArrayList<String> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator") + System.getProperty("line.separator")))
    println("Solution Part 1: " + solvePart1(input))
    println("Solution Part 2: " + solvePart2(input))
    // end::splitInput[]
}

static Long solvePart1(ArrayList<String> input) {
    // tag::solvePart1[]
    Long solution = 1
    HashMap<Integer, Tile> tiles = convertToTiles(input)
    tiles.values().forEach{Tile tile ->
        if(tile.getNumberOfMatchingTiles(tiles) == 2) solution *= tile.getTileNumber() as Long
    }
    return solution
    // end::solvePart1[]
}

static Long solvePart2(ArrayList<String> input) {
    // tag::solvePart2[]
    HashMap<Integer, Tile> tiles = convertToTiles(input)
    ArrayList<ArrayList> picture = createPicture(tiles)
//    printPicture(picture)
    removeBorders(picture)
    Tile pictureAsTile = convertPictureToTile(picture)
    orientateForSeaMonsters(pictureAsTile)
//    pictureAsTile.print()
    return pictureAsTile.countNonMonsterBlack()
    // end::solvePart2[]
}

static void orientSecondTile(Tile first, Tile second) {
    for (int i = 0; i < 8; i++) {
        if(i == 4) second.flipAroundHorizontalAxis()
        if(orientationMatches(first, second)) {
            break
        }
        second.rotateClockwise()
    }
}

static boolean orientationMatches(Tile tile1, Tile tile2) {
    boolean match = false
    if(tile1.getTop() == tile2.getBottom().reverse()) { match = true }
    else if(tile1.getRight() == tile2.getLeft().reverse()) { match = true }
    else if(tile1.getBottom() == tile2.getTop().reverse()) { match = true }
    else if(tile1.getLeft() == tile2.getRight().reverse()) { match = true }
    return match
}

static void printPicture(ArrayList<ArrayList> picture) {
    println("Assambled picture:")
    picture.forEach{ArrayList<Tile> row ->
        for(int i = 0; i < row.get(0).getLeft().length(); i++){
            row.forEach{Tile currentTile ->
                print(currentTile.getRows().get(i) + " ")
            }
            print(System.lineSeparator())
        }
        print(System.lineSeparator())
    }
    print(System.lineSeparator())
}

static void removeBorders(ArrayList<ArrayList> picture) {
    picture.forEach{ArrayList row ->
        row.forEach{Tile tile ->
            tile.removeBorders()
        }
    }
}

static Tile convertPictureToTile(ArrayList<ArrayList> picture) {
    String pictureAsString = ""
    picture.forEach{ArrayList<Tile> row ->
        for(int i = 0; i < row.get(0).getLeft().length(); i++){
            row.forEach{Tile currentTile ->
                pictureAsString += currentTile.getRows().get(i)
            }
            pictureAsString += System.lineSeparator()
        }
    }
    pictureAsString = pictureAsString.trim()
    return new Tile(0, pictureAsString.trim())
}

static Tile getCorner(HashMap tiles) {
    Tile corner = null
    tiles.values().forEach{Tile tile ->
        if(tile.getNumberOfMatchingTiles(tiles) == 2) {
            corner = tile
        }
    }
    return corner
}

static ArrayList<ArrayList> createPicture(HashMap<Integer, Tile> tiles) {
    ArrayList<ArrayList> picture = new ArrayList<>()

    // Get any corner to start creating the picture
    Tile topLeftCorner = getCorner(tiles)
    while(topLeftCorner.getRightMatchingTile(tiles) == null || topLeftCorner.getBottomMatchingTile(tiles) == null) topLeftCorner.rotateClockwise()

    // Get first row of tiles
    ArrayList<Tile> row = getRowOfTiles(topLeftCorner, tiles)
    picture.add(row)

    // Always check if the left tile of the last row has a bottom tile for the next row. If there is no bottom tile, we are in the last row.
    Tile lastLeftTile = topLeftCorner
    while(lastLeftTile.getBottomMatchingTile(tiles) != null) {
        Tile nextLeftTile = lastLeftTile.getBottomMatchingTile(tiles)
        orientSecondTile(lastLeftTile, nextLeftTile)
        row = getRowOfTiles(nextLeftTile, tiles)
        picture.add(row)
        lastLeftTile = nextLeftTile
    }

    return picture
}

static ArrayList<Tile> getRowOfTiles(Tile leftTile, HashMap<Integer, Tile> tiles) {
    ArrayList<Tile> row = new ArrayList<>()
    Tile lastTile = leftTile
    row.add(lastTile)
    while(lastTile.getRightMatchingTile(tiles) != null) {
        Tile nextTile = lastTile.getRightMatchingTile(tiles)
        orientSecondTile(lastTile, nextTile)
        row.add(nextTile)
        lastTile = nextTile
    }
    return row
}

static HashMap<Integer, Tile> convertToTiles(ArrayList<String> tileStrings) {
    HashMap<Integer, Tile> tiles = new HashMap<>()
    tileStrings.forEach{String tileString ->
        Tile tile = new Tile(tileString)
        tiles.put(tile.getTileNumber(), tile)
    }
    return tiles
}

static void orientateForSeaMonsters(Tile tile) {
    for (int i = 0; i < 8; i++) {
        if(i == 4) tile.flipAroundHorizontalAxis()

        // Real data contains one sea monster for wrongly orientated picture. Therefore I try to find more than one sea monster.
        if(tile.countSeaMonsters() > 1) {
            break
        }

        tile.rotateClockwise()
    }
}

static void testPart1() {
    ArrayList<String> input = Arrays.asList(new File("input_test_1.txt").text.split(System.getProperty("line.separator") + System.getProperty("line.separator")))
    HashMap<Integer, Tile> tiles = convertToTiles(input)
    assert tiles.get(2311).getTileNumber() == 2311
    assert tiles.get(2311).getTop() == "..##.#..#."
    assert tiles.get(2311).getRight() == "...#.##..#"
    assert tiles.get(2311).getBottom() == "###..###.."
    assert tiles.get(2311).getLeft() == ".#..#####."
    assert tiles.get(2311).isTileMatching(tiles.get(1951))
    assert tiles.get(2311).isTileMatching(tiles.get(1427))
    assert tiles.get(2311).isTileMatching(tiles.get(3079))
    assert tiles.get(1951).getNumberOfMatchingTiles(tiles) == 2
    assert tiles.get(2311).getNumberOfMatchingTiles(tiles) == 3
    assert tiles.get(3079).getNumberOfMatchingTiles(tiles) == 2
    assert tiles.get(2729).getNumberOfMatchingTiles(tiles) == 3
    assert tiles.get(1427).getNumberOfMatchingTiles(tiles) == 4
    assert tiles.get(2473).getNumberOfMatchingTiles(tiles) == 3
    assert tiles.get(2971).getNumberOfMatchingTiles(tiles) == 2
    assert tiles.get(1489).getNumberOfMatchingTiles(tiles) == 3
    assert tiles.get(1171).getNumberOfMatchingTiles(tiles) == 2
    assert solvePart1(input) == 20899048083289
}

static void testPart2() {
    ArrayList<String> input = Arrays.asList(new File("input_test_1.txt").text.split(System.getProperty("line.separator") + System.getProperty("line.separator")))

    HashMap<Integer, Tile> tiles
    tiles = convertToTiles(input)
    testRotation(tiles)
    tiles = convertToTiles(input)
    testFlipping(tiles)
    tiles = convertToTiles(input)
    testDirectionalMatching(tiles)
    tiles = convertToTiles(input)
    testRemoveBorders(tiles)
    testCountSeamonsters()

    assert solvePart2(input) == 273
}

static void testRotation(HashMap<Integer,Tile> tiles) {
    Tile tile = tiles.get(2311)

    assert tile.getTop() == "..##.#..#."
    assert tile.getRight() == "...#.##..#"
    assert tile.getBottom() == "###..###.."
    assert tile.getLeft() == ".#..#####."

    tile.rotateClockwise()

    assert tile.getTop() == ".#..#####."
    assert tile.getRight() == "..##.#..#."
    assert tile.getBottom() == "...#.##..#"
    assert tile.getLeft() == "###..###.."

    tile.rotateCounterClockwise()

    assert tile.getTop() == "..##.#..#."
    assert tile.getRight() == "...#.##..#"
    assert tile.getBottom() == "###..###.."
    assert tile.getLeft() == ".#..#####."
}

static void testFlipping(HashMap<Integer,Tile> tiles) {
    Tile tile = tiles.get(2311)

    assert tile.getTop() == "..##.#..#."
    assert tile.getRight() == "...#.##..#"
    assert tile.getBottom() == "###..###.."
    assert tile.getLeft() == ".#..#####."

    tile.flipAroundHorizontalAxis()

    assert tile.getTop() == "..###..###"
    assert tile.getRight() == "#..##.#..."
    assert tile.getBottom() == ".#..#.##.."
    assert tile.getLeft() == ".#####..#."

    tile.flipAroundVerticalAxis()

    assert tile.getTop() == "###..###.."
    assert tile.getRight() == ".#..#####."
    assert tile.getBottom() == "..##.#..#."
    assert tile.getLeft() == "...#.##..#"
}

static void testDirectionalMatching(HashMap<Integer,Tile> tiles) {
    Tile tile = tiles.get(1427)

    assert tile.getTopMatchingTile(tiles).getTileNumber() == 1489
    assert tile.getRightMatchingTile(tiles).getTileNumber() == 2473
    assert tile.getBottomMatchingTile(tiles).getTileNumber() == 2311
    assert tile.getLeftMatchingTile(tiles).getTileNumber() == 2729
}

static void testRemoveBorders(HashMap<Integer,Tile> tiles) {
    Tile tile = tiles.get(2311)

    assert tile.getTop() == "..##.#..#."
    assert tile.getRight() == "...#.##..#"
    assert tile.getBottom() == "###..###.."
    assert tile.getLeft() == ".#..#####."

    tile.removeBorders()

    assert tile.getTop() == "#..#...."
    assert tile.getRight() == ".#.###.#"
    assert tile.getBottom() == "#.#...##"
    assert tile.getLeft() == "#.####.#"
}

static void testCountSeamonsters() {
    String tileMonster = "                  # " + System.lineSeparator() +
            "#    ##    ##    ###" + System.lineSeparator() +
            " #  #  #  #  #  #   "
    Tile tile = new Tile(0, tileMonster)
    assert tile.countSeaMonsters() == 1
    assert tile.countBlack() == 15
    assert tile.countNonMonsterBlack() == 0

    tileMonster = "#                 # " + System.lineSeparator() +
            "#    ##    ##    ###" + System.lineSeparator() +
            " #  #  #  #  #  #   " + System.lineSeparator() +
            "                  # " + System.lineSeparator() +
            "#    ##    ##    ###" + System.lineSeparator() +
            " #  #  #  #  #  #   "
    tile = new Tile(0, tileMonster)
    assert tile.countSeaMonsters() == 2
    assert tile.countBlack() == 31
    assert tile.countNonMonsterBlack() == 1
}

class Tile {
    static final int NOT = 0
    static final int TOP = 1
    static final int RIGHT = 2
    static final int BOTTOM = 3
    static final int LEFT = 4

    private int tileNumber
    ArrayList<String> rows
    private String top
    private String right
    private String bottom
    private String left

    Tile(String tile) {
        this.tileNumber = Integer.parseInt(tile.split("Tile ")[1].split(":")[0])

        this.rows = tile.split(System.getProperty("line.separator"))
        this.rows.remove(0)
        initTopRightBottomLeft()
    }

    Tile(int tileNumber, String tile) {
        this.tileNumber = tileNumber

        this.rows = tile.split(System.getProperty("line.separator"))
        initTopRightBottomLeft()
    }

    private initTopRightBottomLeft() {
        this.top = this.rows.get(0)
        this.right = ""
        for(int i = 0; i < this.rows.size(); i++) {
            right += this.rows.get(i).substring(this.rows.get(i).size()-1, this.rows.get(i).size())
        }
        this.bottom = this.rows.get(this.rows.size()-1).reverse()
        this.left = ""
        for(int i = this.rows.size()-1; i >= 0; i--) {
            left += this.rows.get(i).substring(0, 1)
        }
    }

    int getTileNumber() {return this.tileNumber}
    String getTop() {return this.top}
    String getRight() {return this.right}
    String getBottom() {return this.bottom}
    String getLeft() {return this.left}

    int isTileMatching(Tile tile) {
        if(this == tile) return NOT
        int tileMatching = NOT
        if(this.getTop() == tile.getTop()) tileMatching = TOP
        if(this.getTop() == tile.getTop().reverse()) tileMatching = TOP
        if(this.getTop() == tile.getRight()) tileMatching = TOP
        if(this.getTop() == tile.getRight().reverse()) tileMatching = TOP
        if(this.getTop() == tile.getBottom()) tileMatching = TOP
        if(this.getTop() == tile.getBottom().reverse()) tileMatching = TOP
        if(this.getTop() == tile.getLeft()) tileMatching = TOP
        if(this.getTop() == tile.getLeft().reverse()) tileMatching = TOP

        if(this.getRight() == tile.getTop()) tileMatching = RIGHT
        if(this.getRight() == tile.getTop().reverse()) tileMatching = RIGHT
        if(this.getRight() == tile.getRight()) tileMatching = RIGHT
        if(this.getRight() == tile.getRight().reverse()) tileMatching = RIGHT
        if(this.getRight() == tile.getBottom()) tileMatching = RIGHT
        if(this.getRight() == tile.getBottom().reverse()) tileMatching = RIGHT
        if(this.getRight() == tile.getLeft()) tileMatching = RIGHT
        if(this.getRight() == tile.getLeft().reverse()) tileMatching = RIGHT

        if(this.getBottom() == tile.getTop()) tileMatching = BOTTOM
        if(this.getBottom() == tile.getTop().reverse()) tileMatching = BOTTOM
        if(this.getBottom() == tile.getRight()) tileMatching = BOTTOM
        if(this.getBottom() == tile.getRight().reverse()) tileMatching = BOTTOM
        if(this.getBottom() == tile.getBottom()) tileMatching = BOTTOM
        if(this.getBottom() == tile.getBottom().reverse()) tileMatching = BOTTOM
        if(this.getBottom() == tile.getLeft()) tileMatching = BOTTOM
        if(this.getBottom() == tile.getLeft().reverse()) tileMatching = BOTTOM

        if(this.getLeft() == tile.getTop()) tileMatching = LEFT
        if(this.getLeft() == tile.getTop().reverse()) tileMatching = LEFT
        if(this.getLeft() == tile.getRight()) tileMatching = LEFT
        if(this.getLeft() == tile.getRight().reverse()) tileMatching = LEFT
        if(this.getLeft() == tile.getBottom()) tileMatching = LEFT
        if(this.getLeft() == tile.getBottom().reverse()) tileMatching = LEFT
        if(this.getLeft() == tile.getLeft()) tileMatching = LEFT
        if(this.getLeft() == tile.getLeft().reverse()) tileMatching = LEFT
        return tileMatching
    }

    int getNumberOfMatchingTiles(HashMap<Integer, Tile> tiles) {
        int numberOfMatchingTiles = 0
        tiles.values().forEach{
            if(it.getTileNumber() != this.getTileNumber()) {
                if(this.isTileMatching(it) != NOT) numberOfMatchingTiles++
            }
        }
        return numberOfMatchingTiles
    }

    Tile getTopMatchingTile(HashMap<Integer, Tile> tiles) {
        Tile matchingTile = null
        tiles.values().forEach{Tile tile ->
            if(isTileMatching(tile) == TOP) matchingTile = tile
        }
        return matchingTile
    }
    Tile getRightMatchingTile(HashMap<Integer, Tile> tiles) {
        Tile matchingTile = null
        tiles.values().forEach{Tile tile ->
            if(isTileMatching(tile) == RIGHT) matchingTile = tile
        }
        return matchingTile
    }
    Tile getBottomMatchingTile(HashMap<Integer, Tile> tiles) {
        Tile matchingTile = null
        tiles.values().forEach{Tile tile ->
            if(isTileMatching(tile) == BOTTOM) matchingTile = tile
        }
        return matchingTile
    }
    Tile getLeftMatchingTile(HashMap<Integer, Tile> tiles) {
        Tile matchingTile = null
        tiles.values().forEach{Tile tile ->
            if(isTileMatching(tile) == LEFT) matchingTile = tile
        }
        return matchingTile
    }

    void rotateClockwise() {
        ArrayList<String> rotatedRows = new ArrayList<>()
        for(int currentPosition = 0; currentPosition < this.rows.get(0).length(); currentPosition++) {
            String tempRow = ""
            for(int currentRow = this.rows.size()-1; currentRow >= 0; currentRow--) {
                tempRow += this.rows.get(currentRow).substring(currentPosition, currentPosition+1)
            }
            rotatedRows.add(tempRow)
        }
        this.rows = rotatedRows
        initTopRightBottomLeft()
    }
    void rotateCounterClockwise() {
        rotateClockwise()
        rotateClockwise()
        rotateClockwise()
    }

    void flipAroundHorizontalAxis() {
        this.rows = this.rows.reverse()
        initTopRightBottomLeft()
    }
    void flipAroundVerticalAxis() {
        for(int i = 0; i < this.rows.size(); i++) {
            this.rows.set(i, this.rows.get(i).reverse())
        }
        initTopRightBottomLeft()
    }

    void removeBorders() {
        rows.remove(0)
        rows.remove(rows.size() - 1)
        for (int i = 0; i < rows.size(); i++) {
            rows.set(i, rows.get(i).substring(1, rows.get(i).length()-1))
        }
        initTopRightBottomLeft()
    }

    int countSeaMonsters() {
        int seaMonsters = 0
        for (int column = 0; column <= this.rows.get(0).length() - 20; column++) {
            for (int row = 0; row <= this.rows.size() - 3; row++) {
                String pos1 = this.rows.get(row).substring(column+18, column+19)
                String pos2 = this.rows.get(row + 1).substring(column, column+1)
                String pos3 = this.rows.get(row + 1).substring(column+5, column+6)
                String pos4 = this.rows.get(row + 1).substring(column+6, column+7)
                String pos5 = this.rows.get(row + 1).substring(column+11, column+12)
                String pos6 = this.rows.get(row + 1).substring(column+12, column+13)
                String pos7 = this.rows.get(row + 1).substring(column+17, column+18)
                String pos8 = this.rows.get(row + 1).substring(column+18, column+19)
                String pos9 = this.rows.get(row + 2).substring(column+1, column+2)
                String pos10 = this.rows.get(row + 2).substring(column+4, column+5)
                String pos11 = this.rows.get(row + 2).substring(column+7, column+8)
                String pos12 = this.rows.get(row + 2).substring(column+10, column+11)
                String pos13 = this.rows.get(row + 2).substring(column+13, column+14)
                String pos14 = this.rows.get(row + 2).substring(column+16, column+17)
                if(
                    pos1 == "#" &&
                    pos2 == "#" &&
                    pos3 == "#" &&
                    pos4 == "#" &&
                    pos5 == "#" &&
                    pos6 == "#" &&
                    pos7 == "#" &&
                    pos8 == "#" &&
                    pos9 == "#" &&
                    pos10 == "#" &&
                    pos11 == "#" &&
                    pos12 == "#" &&
                    pos13 == "#" &&
                    pos14 == "#"
                ) {
                    seaMonsters++
                }
            }
        }
        return seaMonsters
    }

    int countBlack() {
        int black = 0
        this.rows.forEach{String row ->
            black += row.count("#")
        }
        return black
    }

    int countNonMonsterBlack() {
        return countBlack() - countSeaMonsters() * 15
    }

    void print() {
        println("Tile:")
        this.rows.forEach{String row ->
            println(row)
        }
    }
}
