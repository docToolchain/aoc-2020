import java.util.stream.Collectors
testPart1()
testPart2()
solve()

void solve() {
    // tag::splitInput[]
    ArrayList<String> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator")))
    println("Solution Part 1: " + solvePart1(input))
    println("Solution Part 2: " + solvePart2(input))
    // end::splitInput[]
}

Long solvePart1(ArrayList<String> input) {
    // tag::solvePart1[]
    HashMap rules = getRules(input)
    ArrayList messages = getMessages(input)
    ArrayList parsedRules = parseRule(1, rules.get(0), rules[0], rules, messages)
    return parsedRules.intersect(messages).size()
    // end::solvePart1[]
}

Long solvePart2(ArrayList<String> input) {
    // tag::solvePart2[]
    HashMap<Integer, String> rules = getRules(input)
    int foundMatches = 0

    ArrayList<String> messages = getMessages(input)
    String max = Collections.max(messages, Comparator.comparing(String::length))
    String min = Collections.min(messages, Comparator.comparing(String::length))

    int rule42Length = parseRule(2, rules.get(0), "42", rules, messages).get(0).length()
    ArrayList<String> possibleRulesZero = getPossibleRules(min.length(), max.length(), rule42Length)

    for(int i = 0; i < possibleRulesZero.size(); i++) {
        ArrayList<String> filteredMessages = filterPossibleMessages(messages, possibleRulesZero[i], rule42Length)
        rules.put(0, possibleRulesZero[i])
        ArrayList parsedRules = parseRule(2, rules.get(0), rules[0], rules, filteredMessages)
        foundMatches += parsedRules.intersect(messages).size()
    }
    return foundMatches
    // end::solvePart2[]
}

static HashMap getRules(ArrayList input) {
    HashMap<Integer, String> rules = new HashMap<>()
    int lastRuleIndex = input.indexOf("")
    for(int i = 0; i < lastRuleIndex; i++) {
        String fullRule = input.get(i)
        int ruleNumber = Integer.parseInt(fullRule.split(": ")[0])
        String rule = fullRule.split(": ")[1]
        rules.put(ruleNumber, rule)
    }
    return rules
}

static ArrayList getMessages(ArrayList input) {
    int lastRuleIndex = input.indexOf("")
    return input.subList(lastRuleIndex + 1, input.size())
}

ArrayList<String> parseRule(int part, String rootRule, String rule, HashMap<Integer, String> rules, ArrayList<String> messages) {
    ArrayList<String> parsedRule = new ArrayList<>()
    if(rule.startsWith("\"")) {
        parsedRule.add(rule.substring(1, 2))
    } else {
        ArrayList<String> subRules = Arrays.asList(rule.split(" \\| "))
        subRules.forEach{String subRule ->
            ArrayList<Object> subSubRules = Arrays.asList(subRule.split(" "))
            subSubRules = subSubRules.collect{Object singleRule ->
                parseRule(part, rootRule, rules.get(Integer.parseInt(singleRule as String)), rules, messages)
            }
            if(part == 2 && rootRule == rule) {
                parsedRule = findMessagesInRules(subSubRules as ArrayList<ArrayList>, messages)
            } else {
                ArrayList<String> combinations = subSubRules
                        .combinations()
                        .collect({ subSubRule ->
                            (subSubRule as ArrayList<String>).join()
                        })
                        .stream()
                        .collect(Collectors.toList())
                combinations.forEach{String combo ->
                    parsedRule.add(combo)
                }
            }
        }
    }
    return parsedRule
}

static ArrayList<String> findMessagesInRules(ArrayList<ArrayList> rules, ArrayList<String> messages) {
    ArrayList<String> foundMessages = new ArrayList<>()
    messages.forEach{String message ->
        boolean foundMessage = true
        for(int i = 0; i < rules.size(); i++) {
            int messageSubstringLength = (messages.get(0).length() / rules.size()) as Integer
            String messageSubstring = message.substring(i*messageSubstringLength, i*messageSubstringLength + messageSubstringLength)
            if(!rules.get(i).contains(messageSubstring)) {
                foundMessage = false
            }
        }
        if(foundMessage) foundMessages.add(message)
    }
    return foundMessages
}

void testPart1() {
    ArrayList<String> input = Arrays.asList(new File("input_test_1.txt").text.split(System.getProperty("line.separator")))

    ArrayList<String> messages = getMessages(input)
    assert messages.size() == 5

    HashMap rules = getRules(input)
    assert rules.get(0) == "4 1 5"
    assert rules.get(1) == "2 3 | 3 2"
    assert rules.get(2) == "4 4 | 5 5"
    assert rules.get(3) == "4 5 | 5 4"
    assert rules.get(4) == "\"a\""
    assert rules.get(5) == "\"b\""

    assert parseRule(1, rules.get(0), rules.get(4), rules, messages)[0] == "a"
    assert parseRule(1, rules.get(0), rules.get(5), rules, messages)[0] == "b"

    ArrayList parsedRule = parseRule(1, rules.get(0), rules.get(0), rules, messages)
    assert parsedRule[0] == "aaaabb"
    assert parsedRule[7] == "ababbb"

    assert solvePart1(input) == 2
}

void testPart2() {
    ArrayList<String> input = Arrays.asList(new File("input_test_2.txt").text.split(System.getProperty("line.separator")))
    HashMap<Integer, String> rules = getRules(input)
    ArrayList<String> messages = getMessages(input)

    ArrayList<String> possibleRules = getPossibleRules(15, 45, 5)
    assert possibleRules.size() == 16
    possibleRules = getPossibleRules(24, 96, 8)
    assert possibleRules.size() == 30

    ArrayList<String> filteredMessages = filterPossibleMessages(messages, possibleRules[15], 5)

    assert solvePart1(input) == 3
    assert rules.get(0) == "8 11"
    assert rules.get(1) == "\"a\""
    assert rules.get(2) == "1 24 | 14 4"

    assert parseRule(2, rules.get(0), rules.get(1), rules, filteredMessages)[0] == "a"

    assert solvePart2(input) == 12
}

// standard deep copy implementation
static def deepcopy(orig) {
    Object bos = new ByteArrayOutputStream()
    Object oos = new ObjectOutputStream(bos)
    oos.writeObject(orig); oos.flush()
    Object bin = new ByteArrayInputStream(bos.toByteArray())
    Object ois = new ObjectInputStream(bin)
    return ois.readObject()
}

static ArrayList<String> getPossibleRules(int shortestMessage, int longestMessage, int singleRuleLength) {
    ArrayList<String> possibleRules = new ArrayList<>()
    for(int ruleLength = (shortestMessage/singleRuleLength) as Integer; ruleLength <= longestMessage/singleRuleLength; ruleLength++) {
        int numberOfRules = Math.floor((ruleLength-1)/2) as Integer
        for(int fortyTwoThirtyOne = 1; fortyTwoThirtyOne <= numberOfRules; fortyTwoThirtyOne++) {
            int fortyTwo = ruleLength - fortyTwoThirtyOne * 2
            String rule = ""
            for(int i = 0; i < fortyTwo; i++) {
                rule += "42 "
            }
            for(int i = 0; i < fortyTwoThirtyOne; i++) {
                rule += "42 "
            }
            for(int i = 0; i < fortyTwoThirtyOne; i++) {
                rule += "31 "
            }
            possibleRules.add(rule.substring(0, rule.length()-1))
        }
    }
    return possibleRules
}

static ArrayList<String> filterPossibleMessages(ArrayList<String> messages, String ruleZero, int rule42Length) {
    ArrayList<String> filteredMessages = new ArrayList<>()
    int messageLength = ((ruleZero.length() + 1) / 3 * rule42Length) as Integer
    messages.forEach{
        if(it.length() == messageLength) filteredMessages.add(it)
    }
    return filteredMessages
}