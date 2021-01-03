test()
solve()

void solve() {
    // tag::splitInput[]
    ArrayList<Integer> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator"))).collect{numberAsString ->
        Integer.parseInt(numberAsString)
    }
    // end::splitInput[]


    println("Solution Part 1: " + solvePart1(input))
    println("Solution Part 2: " + solvePart2(input))
}

int solvePart1(ArrayList<Integer> input) {
    // tag::solvePart1[]
    return getOneDifferences(input) * getThreeDifferences(input)
    // end::solvePart1[]
}

Long solvePart2(ArrayList<Integer> input) {
    // tag::solvePart2[]
    input.add(0)
    input.add(input.max() + 3)
    input = input.sort();
    int numberOfOnes = 0
    ArrayList<Integer> factors = new ArrayList<>()
    for (int i = 0; i < input.size() - 1; i++) {
        int diffToNextNumber = input[i+1] - input[i]
        if(diffToNextNumber == 1) {
            numberOfOnes++
        } else {
            if(numberOfOnes > 1) factors.add(getNumberOfPossibilities(numberOfOnes))
            numberOfOnes = 0
        }
    }
    Long product = 1
    factors.forEach { factor ->
        product = product * factor
    }
    return product
    // end::solvePart2[]
}

Integer getOneDifferences(ArrayList<Integer> input) {
    input = input.sort();
    Integer oneDifference = 1
    for (int i = 1; i < input.size(); i++) {
        if(input[i] - input[i-1] == 1) {
            oneDifference++
        }
    }
    return oneDifference
}

Integer getThreeDifferences(ArrayList<Integer> input) {
    input = input.sort();
    Integer threeDifference = 1
    for (int i = 1; i < input.size(); i++) {
        if(input[i] - input[i-1] == 3) {
            threeDifference++
        }
    }
    return threeDifference
}

int getNumberOfPossibilities(int blockSize) {
    int numberOfPossibilities
    switch(blockSize) {
        case 2:
            numberOfPossibilities = 2
            break
        case 3:
            numberOfPossibilities = 4
            break
        case 4:
            numberOfPossibilities = 7
            break
        default:
            println("blocksize: " + blockSize)
            throw new Exception("Fail")
    }
    return numberOfPossibilities
}



void test() {
    ArrayList<Integer> input1 = Arrays.asList(new File('input_test_1.txt').text.split(System.getProperty("line.separator"))).collect{numberAsString ->
        Integer.parseInt(numberAsString)
    }
    ArrayList<Integer> input2 = Arrays.asList(new File('input_test_2.txt').text.split(System.getProperty("line.separator"))).collect{numberAsString ->
        Integer.parseInt(numberAsString)
    }
    assert getOneDifferences(input1) == 7
    assert getThreeDifferences(input1) == 5
    assert solvePart1(input1) == 35
    assert getOneDifferences(input2) == 22
    assert getThreeDifferences(input2) == 10
    assert solvePart1(input2) == 220
    assert solvePart2(input1) == 8
    assert solvePart2(input2) == 19208
}