test()
solve()

void solve() {
    // tag::splitInput[]
    ArrayList<Integer> input = Arrays.asList(16, 1, 0, 18, 12, 14, 19)
    // end::splitInput[]
    println("Solution Part 1: " + solve(input, 2020))
    println("Solution Part 2: " + solve(input, 30000000))
}

Integer solve(ArrayList<Integer> input, int iterations) {
    // tag::solvePart1[]
    HashMap<Integer, Integer> lastIndexOfNumber = new HashMap<>()
    Integer previousNumber
    Integer previousNumberIndex
    for (int i = 0; i < input.size; i++){
        previousNumber = input[i]
        previousNumberIndex = lastIndexOfNumber.get(previousNumber)
        lastIndexOfNumber.put(input[i], i)
    }
    for (int i = input.size(); i < iterations; i++) {
        previousNumber = previousNumberIndex != null ? i - previousNumberIndex - 1 : 0
        previousNumberIndex = lastIndexOfNumber.get(previousNumber)
        lastIndexOfNumber.put(previousNumber, i)
    }
    return previousNumber
    // end::solvePart1[]
}

void test() {
    ArrayList<Integer> input0 = Arrays.asList(0, 3, 6)
    ArrayList<Integer> input1 = Arrays.asList(1, 3, 2)
    ArrayList<Integer> input2 = Arrays.asList(2, 1, 3)
    ArrayList<Integer> input3 = Arrays.asList(1, 2, 3)
    ArrayList<Integer> input4 = Arrays.asList(2, 3, 1)
    ArrayList<Integer> input5 = Arrays.asList(3, 2, 1)
    ArrayList<Integer> input6 = Arrays.asList(3, 1, 2)
    assert solve(input0, 4) == 0
    assert solve(input0, 5) == 3
    assert solve(input0, 6) == 3
    assert solve(input0, 7) == 1
    assert solve(input0, 8) == 0
    assert solve(input0, 9) == 4
    assert solve(input0, 10) == 0
    assert solve(input0, 2020) == 436
    assert solve(input1, 2020) == 1
    assert solve(input2, 2020) == 10
    assert solve(input3, 2020) == 27
    assert solve(input4, 2020) == 78
    assert solve(input5, 2020) == 438
    assert solve(input6, 2020) == 1836
    println("Test part 1 solved")

    assert solve(input0, 30000000) == 175594
    println("input0 solved")
    assert solve(input1, 30000000) == 2578
    println("input1 solved")
    assert solve(input2, 30000000) == 3544142
    println("input2 solved")
    assert solve(input3, 30000000) == 261214
    println("input3 solved")
    assert solve(input4, 30000000) == 6895259
    println("input4 solved")
    assert solve(input5, 30000000) == 18
    println("input5 solved")
    assert solve(input6, 30000000) == 362
    println("input6 solved")
}