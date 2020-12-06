test()
solve()

void solve() {
    // tag::splitInput[]
    ArrayList<String> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator") + System.getProperty("line.separator")))
    // end::splitInput[]
    println("Solution Part 1: " + solvePart1(input))
    println("Solution Part 2: " + solvePart2(input))
}

int solvePart1(ArrayList<String> input) {
    // tag::sumUniqueAnswers[]
    input.collect(answers -> {
        countUniqueAnswers(answers)
    }).value.sum()
    // end::sumUniqueAnswers[]
}

long solvePart2(ArrayList<String> input) {
    // tag::sumCommonAnswers[]
    input.collect(answers -> {
        countCommonAnswers(answers)
    }).value.sum()
    // end::sumCommonAnswers[]
}

void test() {
    ArrayList<String> input = Arrays.asList(new File('input_test.txt').text.split(System.getProperty("line.separator") + System.getProperty("line.separator")))
    assert countUniqueAnswers(input[0]) == 3
    assert countUniqueAnswers(input[1]) == 3
    assert countUniqueAnswers(input[2]) == 3
    assert countUniqueAnswers(input[3]) == 1
    assert countUniqueAnswers(input[4]) == 1
    assert solvePart1(input) == 11

    assert countAnswersPart2(input[0]) == 3
    assert countAnswersPart2(input[1]) == 0
    assert countAnswersPart2(input[2]) == 1
    assert countAnswersPart2(input[3]) == 1
    assert countAnswersPart2(input[4]) == 1
    assert solvePart2(input) == 6
}

int countUniqueAnswers(String answers) {
    // tag::countUniqueAnswers[]
    // Remove the line separators to only have the characters of the answers
    answers = answers.replace(System.getProperty("line.separator"), "")

    // Split String, put it into a HashSet to remove duplicates and return size of HashSet
    return new HashSet<>(Arrays.asList(answers.split("(?!^)"))).size()
    // end::countUniqueAnswers[]
}

int countCommonAnswers(String answers) {
    // tag::countCommonAnswers[]
    // Split answer block to answers of each person in a list
    ArrayList<String> answerList = Arrays.asList(answers.split(System.getProperty("line.separator")))

    // Init list of common answers with each possible answers
    ArrayList<String> commonAnswers = Arrays.asList("abcdefghijklmnopqrstuvwxyz".split("(?!^)"))

    // Intersect common answer list with answers of each person to get the common answers
    answerList.forEach{ answer ->
        commonAnswers = Arrays.asList(answer.split("(?!^)")).intersect(commonAnswers)
    }
    return commonAnswers.size()
    // end::countCommonAnswers[]
}