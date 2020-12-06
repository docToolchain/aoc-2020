
test()
solve()

void solve() {
    ArrayList<String> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator") + System.getProperty("line.separator")))
    println("Solution Part 1: " + solvePart1(input))
    println("Solution Part 2: " + solvePart2(input))
}

int solvePart1(ArrayList<String> input) {
    input.collect(passport -> {
        isPassportValidPart1(passport)
    }).count(true)
}

long solvePart2(ArrayList<String> input) {
    input.collect(passport -> {
        isPassportValidPart2(passport)
    }).count(true)
}

boolean isPassportValidPart1(String passport) {
    // tag::isPassportValidPart1[]
    return     getByr(passport) != null
            && getEyr(passport) != null
            && getIyr(passport) != null
            && getHgt(passport) != null
            && getHcl(passport) != null
            && getEcl(passport) != null
            && getPid(passport) != null
    // end::isPassportValidPart1[]
}

boolean isPassportValidPart2(String passport) {
    // tag::isPassportValidPart2[]
    return     byrValid(getByr(passport))
            && eyrValid(getEyr(passport))
            && iyrValid(getIyr(passport))
            && hgtValid(getHgt(passport))
            && hclValid(getHcl(passport))
            && eclValid(getEcl(passport))
            && pidValid(getPid(passport))
    // end::isPassportValidPart2[]
}

void test() {
    ArrayList<String> input1 = Arrays.asList(new File('input_test1.txt').text.split(System.getProperty("line.separator") + System.getProperty("line.separator")))
    assert getByr(input1[0]) == '1937'
    assert getEyr(input1[0]) == '2020'
    assert getIyr(input1[0]) == '2017'
    assert getHgt(input1[0]) == '183cm'
    assert getHcl(input1[0]) == '#fffffd'
    assert getEcl(input1[0]) == 'gry'
    assert getPid(input1[0]) == '860033327'
    assert getCid(input1[0]) == '147'

    assert getByr(input1[1]) == '1929'
    assert getEyr(input1[1]) == '2023'
    assert getIyr(input1[1]) == '2013'
    assert getHgt(input1[1]) == null
    assert getHcl(input1[1]) == '#cfa07d'
    assert getEcl(input1[1]) == 'amb'
    assert getPid(input1[1]) == '028048884'
    assert getCid(input1[1]) == '350'

    assert solvePart1(input1) == 2

    assert byrValid('1919') == false
    assert byrValid('1920') == true
    assert byrValid('2002') == true
    assert byrValid('2003') == false
    assert byrValid(null) == false

    assert hgtValidCm('149cm') == false
    assert hgtValidCm('150cm') == true
    assert hgtValidCm('193cm') == true
    assert hgtValidCm('194cm') == false
    assert hgtValidCm(null) == false

    assert hgtValidIn('58in') == false
    assert hgtValidIn('59in') == true
    assert hgtValidIn('76in') == true
    assert hgtValidIn('77in') == false
    assert hgtValidIn('160in') == false
    assert hgtValidIn(null) == false

    assert hgtValid('59in') == true
    assert hgtValid('150cm') == true
    assert hgtValid('190') == false
    assert hgtValid('190in') == false
    assert hgtValid(null) == false

    assert hclValid('#123abc') == true
    assert hclValid('#123abz') == false
    assert hclValid('123abc') == false
    assert hclValid(null) == false

    assert eclValid('brn') == true
    assert eclValid('wat') == false
    assert eclValid(null) == false

    assert pidValid('000000001') == true
    assert pidValid('01234567') == false
    assert pidValid('0123456789') == false
    assert pidValid(null) == false

    ArrayList<String> input2 = Arrays.asList(new File('input_test2.txt').text.split(System.getProperty("line.separator") + System.getProperty("line.separator")))
    assert solvePart2(input2) == 0
    ArrayList<String> input3 = Arrays.asList(new File('input_test3.txt').text.split(System.getProperty("line.separator") + System.getProperty("line.separator")))
    assert solvePart2(input3) == 4
}

String getByr(String passport) {
    // tag::getByr[]
    def matcher = passport =~ /byr:(.*?)(\s|$)/
    matcher.find()
    return matcher.size() > 0 ? matcher[0][1] : null
    // end::getByr[]
}

boolean byrValid(String value) {
    // tag::byrValid[]
    def matcher = value =~ /\d{4}/
    matcher.find()
    return matcher.size() > 0 && Integer.parseInt(value) >= 1920 && Integer.parseInt(value) <= 2002
    // end::byrValid[]
}

String getIyr(String passport) {
    def matcher = passport =~ /iyr:(.*?)(\s|$)/
    matcher.find()
    return matcher.size() > 0 ? matcher[0][1] : null
}

boolean iyrValid(String value) {
    def matcher = value =~ /\d{4}/
    matcher.find()
    return matcher.size() > 0 && Integer.parseInt(value) >= 2010 && Integer.parseInt(value) <= 2020
}

String getEyr(String passport) {
    def matcher = passport =~ /eyr:(.*?)(\s|$)/
    matcher.find()
    return matcher.size() > 0 ? matcher[0][1] : null
}

boolean eyrValid(String value) {
    def matcher = value =~ /\d{4}/
    matcher.find()
    return matcher.size() > 0 && Integer.parseInt(value) >= 2020 && Integer.parseInt(value) <= 2030
}

String getHgt(String passport) {
    def matcher = passport =~ /hgt:(.*?)(\s|$)/
    matcher.find()
    return matcher.size() > 0 ? matcher[0][1] : null
}

boolean hgtValid(String value) {
    return hgtValidCm(value) || hgtValidIn(value)
}

boolean hgtValidCm(String value) {
    def matcher = value =~ /(^\d{3})cm$/
    matcher.find()
    return matcher.size() > 0 && Integer.parseInt(matcher[0][1]) >= 150 && Integer.parseInt(matcher[0][1]) <= 193
}

boolean hgtValidIn(String value) {
    def matcher = value =~ /(^\d{2})in$/
    matcher.find()
    return matcher.size() > 0 && Integer.parseInt(matcher[0][1]) >= 59 && Integer.parseInt(matcher[0][1]) <= 76
}

String getHcl(String passport) {
    def matcher = passport =~ /hcl:(.*?)(\s|$)/
    matcher.find()
    return matcher.size() > 0 ? matcher[0][1] : null
}

boolean hclValid(String value) {
    def matcher = value =~ /^#[0-9a-f]{6}$/
    matcher.find()
    return matcher.size() > 0
}

String getEcl(String passport) {
    def matcher = passport =~ /ecl:(.*?)(\s|$)/
    matcher.find()
    return matcher.size() > 0 ? matcher[0][1] : null
}

boolean eclValid(String value) {
    def matcher = value =~ /^(amb|blu|brn|gry|grn|hzl|oth)$/
    matcher.find()
    return matcher.size() > 0
}

String getPid(String passport) {
    def matcher = passport =~ /pid:(.*?)(\s|$)/
    matcher.find()
    return matcher.size() > 0 ? matcher[0][1] : null
}

boolean pidValid(String value) {
    def matcher = value =~ /^\d{9}$/
    matcher.find()
    return matcher.size() > 0 && value.length() == 9
}

String getCid(String passport) {
    def matcher = passport =~ /cid:(.*?)(\s|$)/
    matcher.find()
    return matcher.size() > 0 ? matcher[0][1] : null
}