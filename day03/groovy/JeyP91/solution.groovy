test()
solve()

void solve() {
    ArrayList<String> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator")))
    println("Solution Part 1: " + solvePart1(input))
    println("Solution Part 2: " + solvePart2(input))
}

int solvePart1(ArrayList<String> input) {
    return countTrees(input, 3, 1)
}

long solvePart2(ArrayList<String> input) {
    long trees1 = countTrees(input, 1, 1)
    long trees2 = countTrees(input, 3, 1)
    long trees3 = countTrees(input, 5, 1)
    long trees4 = countTrees(input, 7, 1)
    long trees5 = countTrees(input, 1, 2)
    long solution = trees1 * trees2 * trees3 * trees4 * trees5
    return solution
}

void test() {
    ArrayList<String> input = Arrays.asList(new File('input_test.txt').text.split(System.getProperty("line.separator")))
    assert getTreeForLine(input[0], 0) == 0
    assert getTreeForLine(input[0], 1) == 0
    assert getTreeForLine(input[0], 2) == 1
    assert getTreeForLine(input[0], 11) == 0
    assert getTreeForLine(input[0], 12) == 0
    assert getTreeForLine(input[0], 13) == 1

    assert countTrees(input, 1, 1) == 2
    assert countTrees(input, 3, 1) == 7
    assert countTrees(input, 5, 1) == 3
    assert countTrees(input, 7, 1) == 4
    assert countTrees(input, 1, 2) == 2

    assert solvePart1(input) == 7
    assert solvePart2(input) == 336
}

int getTreeForLine(String line, int index) {
    // tag::patternRepetition[]
    index = index % line.length()
    // end::patternRepetition[]
    // tag::getTreeForLine[]
    String character = line.substring(index, index + 1)    
    String output = ""
    if(character.equals(".")) return 0
    if(character.equals("#")) return 1
    // end::getTreeForLine[]
}

// tag::countTrees[]
int countTrees(ArrayList<String> lines, int right, int down) {
    int count = 0;
    for (int i = 0; i < lines.size(); i = i + down) {
        count += getTreeForLine(lines[i], (int) (i * right / down))
    }
    return count
}
// end::countTrees[]