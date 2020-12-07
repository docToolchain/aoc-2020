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
    ArrayList<Tuple> rules = parseRules(input)
    ArrayList<String> allParentBags = getAllParentBags(rules, "shiny gold")
    return allParentBags.size()
}

int solvePart2(ArrayList<String> input) {
    ArrayList<Tuple> rules = parseRules(input)
    return getAllChildBags(rules, "shiny gold")
}

void test() {
    ArrayList<String> input = Arrays.asList(new File('input_test.txt').text.split(System.getProperty("line.separator")))

    ArrayList<Tuple> rules = parseRules(input)
    assert rules[0][0].equals("light red")
    assert rules[0][1][0].equals(1)
    assert rules[0][1][1].equals("bright white")
    assert rules[1][0].equals("light red")
    assert rules[1][1][0].equals(2)
    assert rules[0][1][1].equals("bright white")

    ArrayList<String> parentBags = getParentBags(rules, "shiny gold")
    assert parentBags[1].equals("bright white")
    assert parentBags[0].equals("muted yellow")

    ArrayList<String> allParentBags = getAllParentBags(rules, "shiny gold")
    assert allParentBags.size() == 4

    ArrayList<Tuple> childBags = getChildBags(rules, "shiny gold")
    assert childBags.size() == 2

    int childBagSum = getAllChildBags(rules, "shiny gold")
    assert childBagSum == 32

    ArrayList<String> input2 = Arrays.asList(new File('input_test_2.txt').text.split(System.getProperty("line.separator")))
    ArrayList<Tuple> rules2 = parseRules(input2)
    childBagSum = getAllChildBags(rules2, "shiny gold")
    assert childBagSum == 126
}

ArrayList<Tuple> parseRule(String rule) {
    // tag::parseRule[]
    ArrayList<Tuple> rules = new ArrayList<>()
    def parentBagMatcher = rule =~ /^(.*?)bag/
    parentBagMatcher.find()
    String parentBag = parentBagMatcher[0][1].trim()

    def childBagMatcher = rule =~ /(\d+)(.*?)bag/
    childBagMatcher.findAll{childBag ->
        rules.add(new Tuple(parentBag, new Tuple(Integer.parseInt(childBag[1]), childBag[2].trim())))
    }
    return rules
    // end::parseRule[]
}

ArrayList<Tuple> parseRules(ArrayList<String> input) {
    ArrayList<Tuple> rules = new ArrayList<>()
    input.forEach(rule ->{
        rules.addAll(parseRule(rule))
    })
    return rules
}

HashSet<String> getParentBags(ArrayList<Tuple> rules, String color) {
    // tag::getParentBags[]
    HashSet<String> parentBags = new HashSet<String>()
    rules.forEach{rule ->
        if(rule[1][1].equals(color)) parentBags.add(rule[0])
    }
    return parentBags
    // end::getParentBags[]
}

HashSet<String> getAllParentBags(ArrayList<Tuple> rules, String color) {
    // tag::getAllParentBags[]
    HashSet<String> parentBags = getParentBags(rules, color)
    HashSet<String> additionalParentBags = new HashSet<String>()
    parentBags.forEach{parentBag ->
        additionalParentBags.addAll(getAllParentBags(rules, parentBag))
    }
    parentBags.addAll(additionalParentBags)
    return parentBags
    // end::getAllParentBags[]
}

ArrayList<Tuple> getChildBags(ArrayList<Tuple> rules, String color) {
    ArrayList<Tuple> childBags = new ArrayList<String>()
    rules.forEach{rule ->
        if(rule[0].equals(color)) childBags.add(new Tuple(rule[1][0], rule[1][1]))
    }
    return childBags
}

int getAllChildBags(ArrayList<Tuple> rules, String color) {
    // tag::getAllChildBags[]
    ArrayList<Tuple> childBags = getChildBags(rules, color)
    int sum = 0
    childBags.forEach{childBag ->
        int childSum = getAllChildBags(rules, childBag[1])
        sum += childBag[0] + childBag[0] * childSum
    }
    return sum
    // end::getAllChildBags[]
}