testPart1()
testPart2()
solve()

static void solve() {
    // tag::splitInput[]
    ArrayList<String> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator")))
    println("Solution Part 1: " + solvePart1(input))
    println("Solution Part 2: " + solvePart2(input))
    // end::splitInput[]
}

static Long solvePart1(ArrayList<String> input) {
    // tag::solvePart1[]
    ArrayList<Integer> player1 = getPlayersCards(input.subList(0, input.indexOf("")) as ArrayList<String>)
    ArrayList<Integer> player2 = getPlayersCards(input.subList(input.indexOf("") + 1, input.size()) as ArrayList<String>)
    while(player1.size() > 0 && player2.size() > 0) {
        playStandard(player1, player2)
    }
    if(player1.size() > 0) return calculatePoints(player1)
    if(player2.size() > 0) return calculatePoints(player2)
    // end::solvePart1[]
}

static Long solvePart2(ArrayList<String> input) {
    // tag::solvePart2[]
    ArrayList<Integer> player1 = getPlayersCards(input.subList(0, input.indexOf("")) as ArrayList<String>)
    ArrayList<Integer> player2 = getPlayersCards(input.subList(input.indexOf("") + 1, input.size()) as ArrayList<String>)

    playRecoursiveCombat(player1, player2)

    if(player1.size() > 0) return calculatePoints(player1)
    if(player2.size() > 0) return calculatePoints(player2)
    // end::solvePart2[]
}

static void playStandard(ArrayList<Integer> player1, ArrayList<Integer> player2) {
    Integer player1Card = player1.remove(0)
    Integer player2Card = player2.remove(0)
    if(player1Card > player2Card) {
        player1.add(player1Card)
        player1.add(player2Card)
    } else {
        player2.add(player2Card)
        player2.add(player1Card)
    }
}

static void playRecoursiveCombat(ArrayList<Integer> player1, ArrayList<Integer> player2) {
    ArrayList<String> player1History = new ArrayList<>()
    ArrayList<String> player2History = new ArrayList<>()
    while(player1.size() > 0 && player2.size() > 0) {
        Integer player1Card = player1.get(0)
        Integer player2Card = player2.get(0)
        String player1Deck = player1.join(" ")
        String player2Deck = player2.join(" ")
        if(player1History.contains(player1Deck) && player2History.contains(player2Deck)) {
            player2.clear()
            break
        }
        else if(player1Card < player1.size() && player2Card < player2.size()) {
            ArrayList<Integer> player1SubDeck = new ArrayList<>(player1)
            player1SubDeck.remove(0)
            player1SubDeck.subList(player1Card, player1SubDeck.size()).clear()

            ArrayList<Integer> player2SubDeck = new ArrayList<>(player2)
            player2SubDeck.remove(0)
            player2SubDeck.subList(player2Card, player2SubDeck.size()).clear()

            playRecoursiveCombat(player1SubDeck, player2SubDeck)

            if(player1SubDeck.size() > 0) {
                player1.add(player1Card)
                player1.add(player2Card)
            } else {
                player2.add(player2Card)
                player2.add(player1Card)
            }
            player1.remove(0)
            player2.remove(0)
        }
        else {
            playStandard(player1, player2)
        }
        player1History.add(player1Deck)
        player2History.add(player2Deck)
    }
}

static int calculatePoints(ArrayList<Integer> cards) {
    int points = 0
    for(int i = 0; i < cards.size(); i++) {
        points += cards.get(i) * (cards.size() - i)
    }
    return points
}

static ArrayList<Integer> getPlayersCards(ArrayList<String> input) {
    input.remove(0)
    return input.collect{Integer.parseInt(it)}
}

static void testPart1() {
    ArrayList<String> input = Arrays.asList(new File("input_test_1.txt").text.split(System.getProperty("line.separator")))
    assert solvePart1(input) == 306
}

static void testPart2() {
    ArrayList<String> input = Arrays.asList(new File("input_test_2.txt").text.split(System.getProperty("line.separator")))
    assert solvePart2(input) == 105
    input = Arrays.asList(new File("input_test_1.txt").text.split(System.getProperty("line.separator")))
    assert solvePart2(input) == 291
}
