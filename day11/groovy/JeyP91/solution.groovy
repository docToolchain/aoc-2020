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
    // tag::solvePart1[]
    ArrayList<String> oldPattern = input
    ArrayList<String> newPattern = calcNextPatternPart1(input)
    while(!isSamePattern(oldPattern, newPattern)) {
        oldPattern = newPattern
        newPattern = calcNextPatternPart1(newPattern)
    }
    return getNumberOfOccupiedSeatsTotal(newPattern)
    // end::solvePart1[]
}

Long solvePart2(ArrayList<String> input) {
    // tag::solvePart2[]
    ArrayList<String> oldPattern = input
    ArrayList<String> newPattern = calcNextPatternPart2(input)
    while(!isSamePattern(oldPattern, newPattern)) {
        oldPattern = newPattern
        newPattern = calcNextPatternPart2(newPattern)
    }
    return getNumberOfOccupiedSeatsTotal(newPattern)
    // end::solvePart2[]
}

boolean isSamePattern(ArrayList<String> pattern1, ArrayList<String> pattern2) {
    def commons = pattern1.intersect(pattern2)
    def difference = pattern1.plus(pattern2)
    difference.removeAll(commons)
    return difference.size() == 0
}

ArrayList<String> calcNextPatternPart1(ArrayList<String> pattern) {
    ArrayList<String> newPattern = new ArrayList<>()
    for(int row = 0; row < pattern.size(); row++) {
        String newRow = ""
        for(int position = 0; position < pattern[row].length(); position++) {
            String oldChar = pattern[row].substring(position, position + 1)
            if (oldChar.equals('.')) {
                newRow += "."
            } else if (oldChar.equals('L')) {
                newRow += getNumberOfOccupiedSeatsPart1(pattern, position, row) == 0 ? "#" : "L"
            } else if (oldChar.equals('#')) {
                newRow += getNumberOfOccupiedSeatsPart1(pattern, position, row) >= 4 ? "L" : "#"
            } else {
                throw new Exception("FAIL")
            }
        }
        newPattern.add(newRow)
    }
    return newPattern
}

int getNumberOfOccupiedSeatsPart1(ArrayList<String> pattern, int position, int row) {
    int occupiedSeats = 0
    ArrayList<Tuple> positionsToCheck = getPositionsToCheckPart1(pattern, position, row)
    positionsToCheck.forEach{ Tuple<Integer> coordinates ->
        int positionCheck = coordinates[0]
        int rowCheck = coordinates[1]
        if(pattern[rowCheck].substring(positionCheck, positionCheck+1).equals('#')) occupiedSeats++
    }
    return occupiedSeats
}

ArrayList<Tuple> getPositionsToCheckPart1(ArrayList<String> pattern, int position, int row) {
    ArrayList<Tuple> positionsToCheck = new ArrayList<>()
    if(isPositionValid(pattern, position-1, row-1)) positionsToCheck.add(new Tuple(position-1, row-1))
    if(isPositionValid(pattern, position-1, row)) positionsToCheck.add(new Tuple(position-1, row))
    if(isPositionValid(pattern, position-1, row+1)) positionsToCheck.add(new Tuple(position-1, row+1))
    if(isPositionValid(pattern, position, row-1)) positionsToCheck.add(new Tuple(position, row-1))
    if(isPositionValid(pattern, position, row+1)) positionsToCheck.add(new Tuple(position, row+1))
    if(isPositionValid(pattern, position+1, row-1)) positionsToCheck.add(new Tuple(position+1, row-1))
    if(isPositionValid(pattern, position+1, row)) positionsToCheck.add(new Tuple(position+1, row))
    if(isPositionValid(pattern, position+1, row+1)) positionsToCheck.add(new Tuple(position+1, row+1))
    return positionsToCheck
}

ArrayList<String> calcNextPatternPart2(ArrayList<String> pattern) {
    ArrayList<String> newPattern = new ArrayList<>()
    for(int row = 0; row < pattern.size(); row++) {
        String newRow = ""
        for(int position = 0; position < pattern[row].length(); position++) {
            String oldChar = pattern[row].substring(position, position + 1)
            if (oldChar.equals('.')) {
                newRow += "."
            } else if (oldChar.equals('L')) {
                newRow += getNumberOfOccupiedSeatsPart2(pattern, position, row) == 0 ? "#" : "L"
            } else if (oldChar.equals('#')) {
                newRow += getNumberOfOccupiedSeatsPart2(pattern, position, row) >= 5 ? "L" : "#"
            } else {
                throw new Exception("FAIL")
            }
        }
        newPattern.add(newRow)
    }
    return newPattern
}

int getNumberOfOccupiedSeatsPart2(ArrayList<String> pattern, int position, int row) {
    int occupiedSeats = 0
    ArrayList<Tuple> positionsToCheck = getPositionsToCheckPart2(pattern, position, row)
    positionsToCheck.forEach{ Tuple<Integer> coordinates ->
        int positionCheck = coordinates[0]
        int rowCheck = coordinates[1]
        if(pattern[rowCheck].substring(positionCheck, positionCheck+1).equals('#')) occupiedSeats++
    }
    return occupiedSeats
}

ArrayList<Tuple> getPositionsToCheckPart2(ArrayList<String> pattern, int position, int row) {
    ArrayList<Tuple> positionsToCheck = new ArrayList<>()
    positionsToCheck.add(getNextSeatInDirection(pattern, position, row, -1, -1))
    positionsToCheck.add(getNextSeatInDirection(pattern, position, row, -1, 0))
    positionsToCheck.add(getNextSeatInDirection(pattern, position, row, -1, 1))
    positionsToCheck.add(getNextSeatInDirection(pattern, position, row, 0, -1))
    positionsToCheck.add(getNextSeatInDirection(pattern, position, row, 0, 1))
    positionsToCheck.add(getNextSeatInDirection(pattern, position, row, 1, -1))
    positionsToCheck.add(getNextSeatInDirection(pattern, position, row, 1, 0))
    positionsToCheck.add(getNextSeatInDirection(pattern, position, row, 1, 1))
    positionsToCheck.removeAll([null])
    return positionsToCheck
}

Tuple<Integer> getNextSeatInDirection(ArrayList<String> pattern, int position, int row, int directionPosition, int directionRow) {
    int offsetCounter = 1
    Tuple<Integer> nextSeat = null
    int nextPosition = position + directionPosition * offsetCounter
    int nextRow = row + directionRow * offsetCounter
    while(isPositionValid(pattern, nextPosition, nextRow)) {
        String seat = pattern[nextRow].substring(nextPosition, nextPosition + 1)
        if(seat != '.') {
            nextSeat = new Tuple(nextPosition, nextRow)
            break
        }
        offsetCounter++
        nextPosition = position + directionPosition * offsetCounter
        nextRow = row + directionRow * offsetCounter
    }
    return nextSeat
}

boolean isPositionValid(ArrayList<String> pattern, int position, int row) {
    return position >= 0 &&
            row >= 0 &&
            row < pattern.size() &&
            position < pattern[row].length()
}

int getNumberOfOccupiedSeatsTotal(ArrayList<String> pattern) {
    int occupiedSeats = 0
    pattern.forEach{ String row ->
        occupiedSeats += row.count('#')
    }
    return occupiedSeats
}

void test() {
    testPart1()
    testPart2()
}

void testPart1() {
    ArrayList<String> input = Arrays.asList(new File('input_test_start.txt').text.split(System.getProperty("line.separator")))

    assert !isPositionValid(input, -1, 0)
    assert !isPositionValid(input, 0, -1)
    assert isPositionValid(input, 0, 0)
    assert isPositionValid(input, 9, 9)
    assert !isPositionValid(input, 9, 10)
    assert !isPositionValid(input, 10, 9)

    ArrayList<String> part1round1should = Arrays.asList(new File('input_test_part1_round1.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> part1round2should = Arrays.asList(new File('input_test_part1_round2.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> part1round3should = Arrays.asList(new File('input_test_part1_round3.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> part1round4should = Arrays.asList(new File('input_test_part1_round4.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> part1round5should = Arrays.asList(new File('input_test_part1_round5.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> part1round1is = calcNextPatternPart1(input)
    ArrayList<String> part1round2is = calcNextPatternPart1(part1round1is)
    ArrayList<String> part1round3is = calcNextPatternPart1(part1round2is)
    ArrayList<String> part1round4is = calcNextPatternPart1(part1round3is)
    ArrayList<String> part1round5is = calcNextPatternPart1(part1round4is)

    assert getNumberOfOccupiedSeatsPart1(input, 0, 0) == 0
    assert getNumberOfOccupiedSeatsPart1(part1round1should, 0, 0) == 2
    assert getNumberOfOccupiedSeatsPart1(part1round2should, 0, 0) == 1
    assert getNumberOfOccupiedSeatsPart1(part1round3should, 0, 0) == 1
    assert getNumberOfOccupiedSeatsPart1(part1round4should, 0, 0) == 1
    assert getNumberOfOccupiedSeatsPart1(part1round5should, 0, 0) == 1
    assert getNumberOfOccupiedSeatsPart1(part1round1should, 1, 1) == 6
    assert getNumberOfOccupiedSeatsPart1(part1round2should, 1, 1) == 2
    assert getNumberOfOccupiedSeatsPart1(part1round3should, 1, 1) == 5
    assert getNumberOfOccupiedSeatsPart1(part1round4should, 1, 1) == 3
    assert getNumberOfOccupiedSeatsPart1(part1round5should, 1, 1) == 4
    assert getNumberOfOccupiedSeatsPart1(part1round1should, 9, 9) == 2
    assert getNumberOfOccupiedSeatsPart1(part1round2should, 9, 9) == 1
    assert getNumberOfOccupiedSeatsPart1(part1round3should, 9, 9) == 1
    assert getNumberOfOccupiedSeatsPart1(part1round4should, 9, 9) == 1
    assert getNumberOfOccupiedSeatsPart1(part1round5should, 9, 9) == 1

    assert isSamePattern(part1round1should, part1round1is)
    assert isSamePattern(part1round2should, part1round2is)
    assert isSamePattern(part1round3should, part1round3is)
    assert isSamePattern(part1round4should, part1round4is)
    assert isSamePattern(part1round5should, part1round5is)
}

void testPart2() {
    ArrayList<String> input = Arrays.asList(new File('input_test_start.txt').text.split(System.getProperty("line.separator")))

    assert getNextSeatInDirection(input, 7, 2, -1, 0) == new Tuple(4, 2)
    assert getNextSeatInDirection(input, 7, 2, 1, 0) == null
    assert getNextSeatInDirection(input, 2, 6, -1, 0) == null
    assert getNextSeatInDirection(input, 8, 0, -1, 1) == new Tuple(5, 3)
    assert getNextSeatInDirection(input, 4, 2, -1, 0) == new Tuple(2, 2)

    ArrayList<String> part2round1should = Arrays.asList(new File('input_test_part2_round1.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> part2round2should = Arrays.asList(new File('input_test_part2_round2.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> part2round3should = Arrays.asList(new File('input_test_part2_round3.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> part2round4should = Arrays.asList(new File('input_test_part2_round4.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> part2round5should = Arrays.asList(new File('input_test_part2_round5.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> part2round6should = Arrays.asList(new File('input_test_part2_round6.txt').text.split(System.getProperty("line.separator")))

    assert getNumberOfOccupiedSeatsPart2(input, 0, 0) == 0
    assert getNumberOfOccupiedSeatsPart2(part2round1should, 1, 1) == 7
    assert getNumberOfOccupiedSeatsPart2(part2round2should, 1, 1) == 2
    assert getNumberOfOccupiedSeatsPart2(part2round3should, 1, 1) == 5
    assert getNumberOfOccupiedSeatsPart2(part2round4should, 1, 1) == 3
    assert getNumberOfOccupiedSeatsPart2(part2round5should, 1, 1) == 3
    assert getNumberOfOccupiedSeatsPart2(part2round6should, 1, 1) == 3

    ArrayList<String> part2round1is = calcNextPatternPart2(input)
    ArrayList<String> part2round2is = calcNextPatternPart2(part2round1is)
    ArrayList<String> part2round3is = calcNextPatternPart2(part2round2is)
    ArrayList<String> part2round4is = calcNextPatternPart2(part2round3is)
    ArrayList<String> part2round5is = calcNextPatternPart2(part2round4is)
    ArrayList<String> part2round6is = calcNextPatternPart2(part2round5is)

    assert isSamePattern(part2round1should, part2round1is)
    assert isSamePattern(part2round2should, part2round2is)
    assert isSamePattern(part2round3should, part2round3is)
    assert isSamePattern(part2round4should, part2round4is)
    assert isSamePattern(part2round5should, part2round5is)
    assert isSamePattern(part2round6should, part2round6is)
}