test()
solve()

void solve() {
    // tag::splitInput[]
    ArrayList<String> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator")))
    // end::splitInput[]
    println("Solution Part 1: " + solvePart1(input))
    println("Solution Part 2: " + solvePart2(input))
}

int solvePart1(ArrayList<String> input) {
    // currentPositionEastWest = 0
    // currentPositionNorthSouth = 0
    // currentDirection = 0
    Tuple<Integer> currentPositionAndDirection = new Tuple(0, 0, 0)
    // tag::solvePart1[]
    input.forEach{String instruction ->
        currentPositionAndDirection = movePart1(currentPositionAndDirection, instruction)
    }
    return Math.abs(currentPositionAndDirection[0] as Integer) + Math.abs(currentPositionAndDirection[1] as Integer)
    // end::solvePart1[]
}

int solvePart2(ArrayList<String> input) {
    // currentPositionEastWest = 0
    // currentPositionNorthSouth = 0
    // currentWaypointOffsetEastWest = 0
    // currentWaypointOffsetNorthSouth = 0
    Tuple<Integer> currentPositionAndDirection = new Tuple(0, 0, 10, 1)
    // tag::solvePart1[]
    input.forEach{String instruction ->
        currentPositionAndDirection = movePart2(currentPositionAndDirection, instruction)
    }
    return Math.abs(currentPositionAndDirection[0] as Integer) + Math.abs(currentPositionAndDirection[1] as Integer)
    // end::solvePart1[]
}

Tuple<Integer> movePart1(Tuple<Integer> currentPositionAndDirection, String instruction){
    int currentPositionEastWest = currentPositionAndDirection[0]
    int currentPositionNorthSouth = currentPositionAndDirection[1]
    int currentDirection = currentPositionAndDirection[2]
    String action = instruction.substring(0, 1)
    int value = Integer.parseInt(instruction.substring(1, instruction.length()))
    switch (action) {
        case 'N':
            currentPositionNorthSouth += value
            break
        case 'S':
            currentPositionNorthSouth -= value
            break
        case 'E':
            currentPositionEastWest += value
            break
        case 'W':
            currentPositionEastWest -= value
            break
        case 'R':
            currentDirection += value
            break
        case 'L':
            currentDirection += 360 - value
            break
        case 'F':
            // East
            if(currentDirection % 360 == 0) {
                currentPositionEastWest += value
            }
            // South
            if(currentDirection % 360 == 90) {
                currentPositionNorthSouth -= value
            }
            // West
            if(currentDirection % 360 == 180) {
                currentPositionEastWest -= value
            }
            // North
            if(currentDirection % 360 == 270) {
                currentPositionNorthSouth += value
            }
            break
        default:
            throw new Exception("FAIL")
    }
    return new Tuple(currentPositionEastWest, currentPositionNorthSouth, currentDirection)
}

Tuple<Integer> movePart2(Tuple<Integer> currentPositionAndDirection, String instruction){
    int currentPositionEastWest = currentPositionAndDirection[0]
    int currentPositionNorthSouth = currentPositionAndDirection[1]
    int currentWaypointOffsetEastWest = currentPositionAndDirection[2]
    int currentWaypointOffsetNorthSouth = currentPositionAndDirection[3]
    String action = instruction.substring(0, 1)
    int value = Integer.parseInt(instruction.substring(1, instruction.length()))
    switch (action) {
        case 'N':
            currentWaypointOffsetNorthSouth += value
            break
        case 'S':
            currentWaypointOffsetNorthSouth -= value
            break
        case 'E':
            currentWaypointOffsetEastWest += value
            break
        case 'W':
            currentWaypointOffsetEastWest -= value
            break
        case 'R':
            Tuple newWaypointOffset = calculateNewWaypointOffset(currentWaypointOffsetEastWest, currentWaypointOffsetNorthSouth, value)
            currentWaypointOffsetEastWest = newWaypointOffset[0]
            currentWaypointOffsetNorthSouth = newWaypointOffset[1]
            break
        case 'L':
            Tuple<Integer> newWaypointOffset = calculateNewWaypointOffset(currentWaypointOffsetEastWest, currentWaypointOffsetNorthSouth, 360 - value)
            currentWaypointOffsetEastWest = newWaypointOffset[0]
            currentWaypointOffsetNorthSouth = newWaypointOffset[1]
            break
        case 'F':
            currentPositionEastWest = currentPositionEastWest + currentWaypointOffsetEastWest * value
            currentPositionNorthSouth = currentPositionNorthSouth + currentWaypointOffsetNorthSouth * value
            break
        default:
            throw new Exception("FAIL")
    }
    return new Tuple(currentPositionEastWest, currentPositionNorthSouth, currentWaypointOffsetEastWest, currentWaypointOffsetNorthSouth)
}

Tuple<Integer> calculateNewWaypointOffset(int currentWaypointOffsetEastWest, int currentWaypointOffsetNorthSouth, int rotationValue) {
    switch (rotationValue) {
        case 90:
            int temp = currentWaypointOffsetEastWest
            currentWaypointOffsetEastWest = currentWaypointOffsetNorthSouth
            currentWaypointOffsetNorthSouth = temp * -1
            break
        case 180:
            currentWaypointOffsetEastWest = currentWaypointOffsetEastWest * -1
            currentWaypointOffsetNorthSouth = currentWaypointOffsetNorthSouth * -1
            break
        case 270:
            int temp = currentWaypointOffsetEastWest
            currentWaypointOffsetEastWest = currentWaypointOffsetNorthSouth * -1
            currentWaypointOffsetNorthSouth = temp
            break
        default:
            throw new Exception("FAIL")
    }
    return new Tuple<Integer>(currentWaypointOffsetEastWest, currentWaypointOffsetNorthSouth)
}

void test() {
    ArrayList<String> input = Arrays.asList(new File('input_test.txt').text.split(System.getProperty("line.separator")))
    assert solvePart1(input) == 25
    assert solvePart2(input) == 286
}