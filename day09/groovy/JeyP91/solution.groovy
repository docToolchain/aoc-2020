test()
solve()

void solve() {
    // tag::splitInput[]
    ArrayList<Long> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator"))).collect{numberAsString ->
        Long.parseLong(numberAsString)
    }

    // end::splitInput[]
    println("Solution Part 1: " + solvePart1(input, 25))
    println("Solution Part 2: " + solvePart2(input, 25))
}

Long solvePart1(ArrayList<Long> input, int preamble) {
    // tag::solvePart1[]
    Long numberWithoutSum = 0
    for(int i = preamble; i < input.size(); i++) {
        boolean sumFound = false
        for (int summand1 = i-preamble; summand1 < i; summand1++) {
            for (int summand2 = summand1 + 1; summand2 < i; summand2++) {
                if(input[summand1] + input[summand2] == input[i]) {
                    sumFound = true
                }
            }
        }
        if(!sumFound) {
            numberWithoutSum = input[i]
            break
        }
    }
    return numberWithoutSum
    // end::solvePart1[]
}

int solvePart2(ArrayList<Long> input, int preamble) {
    // tag::solvePart2[]
    int missingSum = solvePart1(input, preamble)
    int solution
    for(int i = 0; i < input.size(); i++) {
        int tempSum = input[i]
        int smallestNumber = input[i]
        int largestNumber = input[i]
        int sumCounter = 0
        while(tempSum < missingSum) {
            sumCounter++
            tempSum += input[i + sumCounter]
            if(input[i + sumCounter] < smallestNumber) smallestNumber = input[i + sumCounter]
            if(input[i + sumCounter] > largestNumber) largestNumber = input[i + sumCounter]
        }
        if(tempSum == missingSum) {
            solution = smallestNumber + largestNumber
            break
        }
    }
    return solution
    // end::solvePart2[]
}

void test() {
    ArrayList<Long> input = Arrays.asList(new File('input_test.txt').text.split(System.getProperty("line.separator"))).collect{numberAsString ->
        Long.parseLong(numberAsString)
    }
    assert solvePart1(input, 5) == 127
    assert solvePart2(input, 5) == 62
}