test()
solve()

void solve() {
    // tag::splitInput[]
    ArrayList<String> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator")))
    // end::splitInput[]
    println("Solution Part 1: " + solvePart1(input))
    println("Solution Part 2: " + solvePart2(input))
}

Long solvePart1(ArrayList<String> input) {
    // tag::solvePart1[]
    ArrayList<String> rules = getRules(input)
    ArrayList<ArrayList> parsedRules = parseRules(rules)
    // end::solvePart1[]
}

Long solvePart2(ArrayList<String> input) {
    // tag::solvePart2[]
    return 0
    // end::solvePart2[]
}

ArrayList<String> getRules(ArrayList<String> input) {
    int indexRules = input.indexOf("")
    return input.subList(0, indexRules)
}

String getMyTicket(ArrayList<String> input) {
    int indexMyTicket = input.indexOf("your ticket:") + 1
    return input[indexMyTicket]
}

ArrayList<String> getNearbyTickets(ArrayList<String> input) {
    int indexNearbyTickets = input.indexOf("nearby tickets:")
    return input.subList(indexNearbyTickets + 1, input.size())
}

ArrayList<ArrayList> parseRules(ArrayList<String> rules) {
    ArrayList<ArrayList> rulesList = new ArrayList<>()
    rules.forEach{
        rulesList.add(parseRule(it))
    }
    return rulesList
}

ArrayList<Integer> parseRule(String rule) {
    ArrayList<Integer> ruleNumbers = new ArrayList<Integer>()
    rule = rule.split(": ")[1]
    ruleNumbers.add(Integer.parseInt(rule.split(' or ')[0].split('-')[0]))
    ruleNumbers.add(Integer.parseInt(rule.split(' or ')[0].split('-')[1]))
    ruleNumbers.add(Integer.parseInt(rule.split(' or ')[1].split('-')[0]))
    ruleNumbers.add(Integer.parseInt(rule.split(' or ')[1].split('-')[1]))
    return ruleNumbers
}

boolean validateTicket(ArrayList<ArrayList> rules, String ticket) {
    boolean validated = true
    Arrays.asList(ticket.split(',')).forEach{String number ->
        validated = validated && validateNumber(rules, Integer.parseInt(number))
    }
    return validated
}

boolean validateNumber(ArrayList<ArrayList> rules, int number) {
    boolean validated = false
    rules.forEach{ArrayList<Integer> rule ->
        validated = validated || validateNumberWithRule(rule, number)
    }
    return validated
}

boolean validateNumberWithRule(ArrayList<Integer> rule, int number) {
    if(number == 8) {
        println("")
    }
    boolean validated = number >= rule [0] && number <= rule[1] ||
            number >= rule [2] && number <= rule[3]
    return validated
}

void test() {
    ArrayList<String> input = Arrays.asList(new File('input_test.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> rules = getRules(input)
    ArrayList<ArrayList> parsedRules = parseRules(rules)
    String myTicket = getMyTicket(input)
    ArrayList<String> nearbyTickets = getNearbyTickets(input)

    assert rules.size() == 3
    assert myTicket == "7,1,14"
    assert nearbyTickets.size() == 4

    assert parseRule("class: 1-3 or 5-7")[0] == 1
    assert parseRule("class: 1-3 or 5-7")[1] == 3
    assert parseRule("class: 1-3 or 5-7")[2] == 5
    assert parseRule("class: 1-3 or 5-7")[3] == 7

    assert parsedRules[0][0] == 1
    assert parsedRules[0][1] == 3
    assert parsedRules[0][2] == 5
    assert parsedRules[0][3] == 7
    assert parsedRules[1][0] == 6
    assert parsedRules[1][1] == 11
    assert parsedRules[1][2] == 33
    assert parsedRules[1][3] == 44

    assert validateNumber(parsedRules, 0) == false
    assert validateNumber(parsedRules, 1) == true
    assert validateNumber(parsedRules, 2) == true
    assert validateNumber(parsedRules, 3) == true
    assert validateNumber(parsedRules, 4) == false
    assert validateNumber(parsedRules, 5) == true
    assert validateNumber(parsedRules, 6) == true
    assert validateNumber(parsedRules, 7) == true
    assert validateNumber(parsedRules, 8) == true

    assert validateTicket(parsedRules, myTicket) == true
    assert validateTicket(parsedRules, nearbyTickets[0]) == true
    assert validateTicket(parsedRules, nearbyTickets[1]) == false
    assert validateTicket(parsedRules, nearbyTickets[2]) == false
    assert validateTicket(parsedRules, nearbyTickets[3]) == false

    assert solvePart1(input) == 0

    assert solvePart2(input) == 0
}