import groovyjarjarantlr4.v4.runtime.misc.Tuple

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
    int earliestTimestamp = Integer.parseInt(input[0])
    ArrayList<Integer> departuresInt = filterDepartures(input)
    int earliestLine = 99999999
    int earliestDeparture = 99999999
    departuresInt.forEach{ int departure ->
        int diff = departure - earliestTimestamp % departure
        if(diff < earliestDeparture) {
            earliestDeparture = diff
            earliestLine = departure
        }
    }
    return earliestLine * earliestDeparture
    // end::solvePart1[]
}

Long solvePart2(ArrayList<String> input) {
    // tag::solvePart2[]
    ArrayList<String> departures = Arrays.asList(input[1].split(','))
    ArrayList<groovy.lang.Tuple> departuresTuples = getTuples(departures)
    Long lastOffset = 0
    Long jump = 1
    for(int i = 1; i <= departuresTuples.size(); i++) {
        Long matchingTimestamp = lastOffset
        while(true) {
            if(verifyTimestamp(departuresTuples.take(i) as ArrayList<Tuple>, matchingTimestamp)) break
            matchingTimestamp += jump
        }
        lastOffset = matchingTimestamp
        jump = jump * departuresTuples[i-1][0]
    }
    return lastOffset
    // end::solvePart2[]
}

ArrayList<groovy.lang.Tuple> getTuples(ArrayList<String> departures) {
    ArrayList<groovy.lang.Tuple> tuples = new ArrayList<>()
    for(int i = 0; i < departures.size(); i++) {
        if(departures[i] != 'x') {
            tuples.add(new groovy.lang.Tuple(Integer.parseInt(departures[i]), i))
        }
    }
    return tuples
}

ArrayList<Integer> filterDepartures(ArrayList<String> input) {
    ArrayList<String> departures = input[1].split(',')
    departures.removeAll{it == 'x'}
    ArrayList<Integer> departuresInt = departures.collect{
        Integer.parseInt(it)
    }
    return departuresInt
}

boolean verifyTimestamp(ArrayList<Tuple> departures, Long departureTimestamp) {
    boolean verified = true
    for(int i = 0; i < departures.size(); i++) {
        verified = (departureTimestamp + departures[i][1]) % departures[i][0] == 0
        if(!verified) break
    }
    return verified
}

void test() {
    ArrayList<String> input1 = Arrays.asList(new File('input_test_1.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> input2 = Arrays.asList(new File('input_test_2.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> input3 = Arrays.asList(new File('input_test_3.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> input4 = Arrays.asList(new File('input_test_4.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> input5 = Arrays.asList(new File('input_test_5.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> input6 = Arrays.asList(new File('input_test_6.txt').text.split(System.getProperty("line.separator")))
    assert solvePart1(input1) == 295
    assert solvePart2(input1) == 1068781
    assert solvePart2(input2) == 3417
    assert solvePart2(input3) == 754018
    assert solvePart2(input4) == 779210
    assert solvePart2(input5) == 1261476
    assert solvePart2(input6) == 1202161486
}