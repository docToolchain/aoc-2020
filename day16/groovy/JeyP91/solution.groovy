testPart1()
testPart2()
solve()

void solve() {
    // tag::splitInput[]
    ArrayList<String> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator")))
    // end::splitInput[]
    println("Solution Part 1: " + solvePart1(input))
    println("Solution Part 2: " + solvePart2(input, "departure", 6))
}

int solvePart1(ArrayList<String> input) {
    // tag::solvePart1[]
    ArrayList<String> rules = getRules(input)
    ArrayList<ArrayList> parsedRules = parseRules(rules)
    ArrayList<String> nearbyTickets = getNearbyTickets(input)
    int errorRate = 0
    nearbyTickets.forEach{String ticket ->
        errorRate += validateTicket(parsedRules, ticket)
    }
    return errorRate
    // end::solvePart1[]
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
    if(rule != "") {
        rule = rule.split(": ")[1]
        ruleNumbers.add(Integer.parseInt(rule.split(' or ')[0].split('-')[0]))
        ruleNumbers.add(Integer.parseInt(rule.split(' or ')[0].split('-')[1]))
        ruleNumbers.add(Integer.parseInt(rule.split(' or ')[1].split('-')[0]))
        ruleNumbers.add(Integer.parseInt(rule.split(' or ')[1].split('-')[1]))
    }
    return ruleNumbers
}

int validateTicket(ArrayList<ArrayList> rules, String ticket) {
    int invalidSum = 0
    Arrays.asList(ticket.split(',')).forEach{String numberString ->
        int number = Integer.parseInt(numberString)
        boolean validated = validateNumber(rules, number)
        if(!validated) {
            invalidSum += number
        }
    }
    return invalidSum
}

boolean validateNumber(ArrayList<ArrayList> rules, int number) {
    boolean validated = false
    rules.forEach{ArrayList<Integer> rule ->
        validated = validated || validateNumberWithRule(rule, number)
    }
    return validated
}

boolean validateNumberWithRule(ArrayList<Integer> rule, int number) {
    boolean validated = false
    if(rule.size() > 0) {
        validated = number >= rule[0] && number <= rule[1] ||
                number >= rule[2] && number <= rule[3]
    }
    return validated
}

Long solvePart2(ArrayList<String> input, String ruleStarter, int numberOfRules) {
    // tag::solvePart2[]
    ArrayList<String> rules = getRules(input)
    ArrayList<ArrayList> parsedRules = parseRules(rules)
    ArrayList<String> nearbyTickets = getNearbyTickets(input)
    ArrayList<String> validTickets = getValidTickets(parsedRules, nearbyTickets)
    String myTicket = getMyTicket(input)
    HashMap postitionRuleMatcher = getPositionRuleMatching(rules, validTickets, ruleStarter, numberOfRules)
    Long solution = 1
    postitionRuleMatcher.forEach{String rule, int position ->
        Long numberAtPosition = Integer.parseInt(myTicket.split(',')[position])
        solution *= numberAtPosition
    }
    return solution
    // end::solvePart2[]
}

ArrayList<String> getValidTickets(ArrayList<ArrayList> parsedRules, ArrayList<String> nearbyTickets) {
    ArrayList<String> validTickets = new ArrayList<>()
    nearbyTickets.forEach{String ticket ->
        if(validateTicket(parsedRules, ticket) == 0) {
            validTickets.add(ticket)
        }
    }
    return validTickets
}

ArrayList<Integer> getValuesForPosition(ArrayList<String> tickets, int position) {
    ArrayList<Integer> values = new ArrayList<>()
    tickets.forEach{ String ticket ->
        values.add(Integer.parseInt(Arrays.asList(ticket.split(','))[position]))
    }
    return values
}

int getRuleForValues(ArrayList<String> rules, ArrayList<Integer> values) {
    int matchingRule = -1
    for(int i = 0; i < rules.size(); i++) {
        ArrayList<Integer> parsedRule = parseRule(rules[i])
        boolean valid = true
        values.forEach{Integer value ->
            valid = valid && validateNumberWithRule(parsedRule, value)
        }
        if(valid) {
            if(matchingRule == -1) {
                matchingRule = i
            } else {
                matchingRule = -1
                break
            }
        }
    }
    return matchingRule
}

HashMap getPositionRuleMatching(ArrayList<String> rules, ArrayList<String> validTickets, String ruleStarter, int numberOfRules) {
    HashMap postitionRuleMatcher = new HashMap()
    int numberOfPositions = Arrays.asList(validTickets[0].split(',')).size()
    int currentPosition = 0
    while(getRulesStartingWith(postitionRuleMatcher, ruleStarter).size() < numberOfRules) {
        ArrayList<Integer> values = getValuesForPosition(validTickets, currentPosition)
        int rule = getRuleForValues(rules, values)
        if(rule > -1) {
            String ruleName = rules[rule].substring(0, rules[rule].indexOf(':'))
            rules[rule] = ""
            postitionRuleMatcher.put(ruleName, currentPosition)
        }
        currentPosition++
        if(currentPosition == numberOfPositions) currentPosition = 0
    }
    return getRulesStartingWith(postitionRuleMatcher, ruleStarter)
}

HashMap getRulesStartingWith(HashMap postitionRuleMatcher, String ruleStarter) {
    HashMap matchingRules = new HashMap()
    postitionRuleMatcher.forEach{String key, Integer value ->
        if(key.startsWith(ruleStarter)) matchingRules.put(key, value)
    }
    return matchingRules
}

void testPart1() {
    ArrayList<String> input = Arrays.asList(new File('input_test_1.txt').text.split(System.getProperty("line.separator")))
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

    assert validateNumberWithRule(parsedRules[0], 0) == false
    assert validateNumberWithRule(parsedRules[0], 1) == true
    assert validateNumberWithRule(parsedRules[0], 2) == true
    assert validateNumberWithRule(parsedRules[0], 3) == true
    assert validateNumberWithRule(parsedRules[0], 4) == false
    assert validateNumberWithRule(parsedRules[0], 5) == true
    assert validateNumberWithRule(parsedRules[0], 6) == true
    assert validateNumberWithRule(parsedRules[0], 7) == true
    assert validateNumberWithRule(parsedRules[0], 8) == false

    assert validateNumber(parsedRules, 50) == true

    assert validateTicket(parsedRules, myTicket) == 0
    assert validateTicket(parsedRules, nearbyTickets[0]) == 0
    assert validateTicket(parsedRules, nearbyTickets[1]) == 4
    assert validateTicket(parsedRules, nearbyTickets[2]) == 55
    assert validateTicket(parsedRules, nearbyTickets[3]) == 12

    assert solvePart1(input) == 71
}

void testPart2() {
    ArrayList<String> input = Arrays.asList(new File('input_test_2.txt').text.split(System.getProperty("line.separator")))
    ArrayList<String> rules = getRules(input)
    ArrayList<ArrayList> parsedRules = parseRules(rules)
    ArrayList<String> nearbyTickets = getNearbyTickets(input)

    ArrayList<String> validTickets = getValidTickets(parsedRules, nearbyTickets)
    HashMap postitionRuleMatcher = getPositionRuleMatching(rules, validTickets, "", 3)

    assert postitionRuleMatcher.get("row") == 0
    assert postitionRuleMatcher.get("class") == 1
    assert postitionRuleMatcher.get("seat") == 2

    assert solvePart2(input, "", 3) == 1716
}