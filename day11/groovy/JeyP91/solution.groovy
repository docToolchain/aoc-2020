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
    ArrayList<String> newPattern = calcNextPattern(input)
    while(!isSamePattern(oldPattern, newPattern)) {
        oldPattern = newPattern
        newPattern = calcNextPattern(newPattern)
    }
    return getNumberOfOccupiedSeatsTotal(newPattern)
    // end::solvePart1[]
}

Long solvePart2(ArrayList<String> input) {
    // tag::solvePart2[]
    return 0
    // end::solvePart2[]
}

boolean isSamePattern(ArrayList<String> pattern1, ArrayList<String> pattern2) {
    def commons = pattern1.intersect(pattern2)
    def difference = pattern1.plus(pattern2)
    difference.removeAll(commons)
    return difference.size() == 0
}

ArrayList<String> calcNextPattern(ArrayList<String> pattern) {
    ArrayList<String> newPattern = new ArrayList<>()
    for(int row = 0; row < pattern.size(); row++) {
        String newRow = ""
        for(int position = 0; position < pattern[row].length(); position++) {
            String oldChar = pattern[row].substring(position, position + 1)
            if (oldChar.equals('.')) {
                newRow += "."
            } else if (oldChar.equals('L')) {
                newRow += getNumberOfOccupiedSeats(pattern, row, position) == 0 ? "#" : "L"
            } else if (oldChar.equals('#')) {
                newRow += getNumberOfOccupiedSeats(pattern, row, position) >= 4 ? "L" : "#"
            } else {
                throw new Exception("FAIL")
            }
        }
        newPattern.add(newRow)
    }
    return newPattern
}

int getNumberOfOccupiedSeats(ArrayList<String> pattern, int posX, int posY) {
    int occupiedSeats = 0
    if(posX>0) {
        if(posY>0 && pattern[posX-1].substring(posY-1, posY).equals('#')) occupiedSeats++
        if(pattern[posX-1].substring(posY, posY+1).equals('#')) occupiedSeats++
        if(posY != pattern[posX-1].length()-1 && pattern[posX-1].substring(posY+1, posY+2).equals('#')) occupiedSeats++
    }
    if(posY>0 && pattern[posX].substring(posY-1, posY).equals('#')) occupiedSeats++
    if(posY != pattern[posX].length()-1 && pattern[posX].substring(posY+1, posY+2).equals('#')) occupiedSeats++

    if(posX < pattern.size()-1) {
        if(posY>0 && pattern[posX+1].substring(posY-1, posY).equals('#')) occupiedSeats++
        if(pattern[posX+1].substring(posY, posY+1).equals('#')) occupiedSeats++
        if(posY != pattern[posX+1].length()-1 && pattern[posX+1].substring(posY+1, posY+2).equals('#')) occupiedSeats++
    }

    return occupiedSeats
}

int getNumberOfOccupiedSeatsTotal(ArrayList<String> pattern) {
    int occupiedSeats = 0
    pattern.forEach{ String row ->
        occupiedSeats += row.count('#')
    }
    return occupiedSeats
}

void test() {
    ArrayList<String> input = Arrays.asList(new File('input_test_start.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> round1should = Arrays.asList(new File('input_test_round1.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> round2should = Arrays.asList(new File('input_test_round2.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> round3should = Arrays.asList(new File('input_test_round3.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> round4should = Arrays.asList(new File('input_test_round4.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> round5should = Arrays.asList(new File('input_test_round5.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> round1is = calcNextPattern(input)
    ArrayList<String> round2is = calcNextPattern(round1is)
    ArrayList<String> round3is = calcNextPattern(round2is)
    ArrayList<String> round4is = calcNextPattern(round3is)
    ArrayList<String> round5is = calcNextPattern(round4is)

    assert getNumberOfOccupiedSeats(input, 0, 0) == 0
    assert getNumberOfOccupiedSeats(round1should, 0, 0) == 2
    assert getNumberOfOccupiedSeats(round2should, 0, 0) == 1
    assert getNumberOfOccupiedSeats(round3should, 0, 0) == 1
    assert getNumberOfOccupiedSeats(round4should, 0, 0) == 1
    assert getNumberOfOccupiedSeats(round5should, 0, 0) == 1
    assert getNumberOfOccupiedSeats(round1should, 1, 1) == 6
    assert getNumberOfOccupiedSeats(round2should, 1, 1) == 2
    assert getNumberOfOccupiedSeats(round3should, 1, 1) == 5
    assert getNumberOfOccupiedSeats(round4should, 1, 1) == 3
    assert getNumberOfOccupiedSeats(round5should, 1, 1) == 4
    assert getNumberOfOccupiedSeats(round1should, 9, 9) == 2
    assert getNumberOfOccupiedSeats(round2should, 9, 9) == 1
    assert getNumberOfOccupiedSeats(round3should, 9, 9) == 1
    assert getNumberOfOccupiedSeats(round4should, 9, 9) == 1
    assert getNumberOfOccupiedSeats(round5should, 9, 9) == 1

    assert isSamePattern(round1should, round1is)
    assert isSamePattern(round2should, round2is)
    assert isSamePattern(round3should, round3is)
    assert isSamePattern(round4should, round4is)
    assert isSamePattern(round5should, round5is)
}