#!/usr/bin/env groovy

test()
solve()

int getFirstNumber(String line) {
    return Integer.parseInt(line.split('-')[0])
}

int getSecondNumber(String line) {
    return Integer.parseInt(line.split('-')[1].split(' ')[0])
}

String getCharacter(String line) {
    return line.split(' ')[1].substring(0,1)
}

String getPassword(String line) {
    return line.split(': ')[1]
}

boolean validatePart1(line) {
    // tag::validatePart1[]
    int min = getFirstNumber(line)
    int max = getSecondNumber(line)
    String character = getCharacter(line)
    String password = getPassword(line)

    int appearances = password.count(character)

    return appearances >= min && appearances <= max
    // end::validatePart1[]
}

boolean validatePart2(line) {
    // tag::validatePart2[]
    int pos1 = getFirstNumber(line)
    int pos2 = getSecondNumber(line)
    String character = getCharacter(line)
    String password = getPassword(line)

    String charPos1 = password.substring(pos1 - 1, pos1)
    String charPos2 = password.substring(pos2 - 1, pos2)

    return character.equals(charPos1) ^ character.equals(charPos2)
    // end::validatePart2[]
}

void test() {
    String testLine

    testLine = "1-3 a: abcde"
    assert getFirstNumber(testLine) == 1
    assert getSecondNumber(testLine) == 3
    assert getCharacter(testLine).equals("a")
    assert getPassword(testLine).equals("abcde")
    assert validatePart1(testLine) == true
    assert validatePart2(testLine) == true

    testLine = "1-3 b: cdefg"
    assert getFirstNumber(testLine) == 1
    assert getSecondNumber(testLine) == 3
    assert getCharacter(testLine).equals("b")
    assert getPassword(testLine).equals("cdefg")
    assert validatePart1(testLine) == false
    assert validatePart2(testLine) == false

    testLine = "2-9 c: ccccccccc"
    assert getFirstNumber(testLine) == 2
    assert getSecondNumber(testLine) == 9
    assert getCharacter(testLine).equals("c")
    assert getPassword(testLine).equals("ccccccccc")
    assert validatePart1(testLine) == true
    assert validatePart2(testLine) == false
}

void solve() {
    ArrayList<String> input = Arrays.asList(new File('input.txt').text.split("\n"))
    int correctPasswordsPart1 = 0;
    int correctPasswordsPart2 = 0;
    for (int i = 0; i < input.size(); i++) {
        if(validatePart1(input[i])) {
            correctPasswordsPart1++;
        }
        if(validatePart2(input[i])) {
            correctPasswordsPart2++;
        }
    }
    println "Solution Part 1: " + correctPasswordsPart1
    println "Solution Part 2: " + correctPasswordsPart2
}