import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

import static java.util.stream.Collectors.toList;

public class Day22 {
//tag::mainPart1[]
    public static void main(String[] args) throws IOException {
        List<String> input = Files.readAllLines(Path.of("day22.txt"));

        List<Integer> cardsP1 = input.stream().skip(1)
                .takeWhile(l -> !l.isBlank())
                .map(Integer::parseInt)
                .collect(toList());
        List<Integer> cardsP2 = input.stream()
                .skip(cardsP1.size() + 3)
                .map(Integer::parseInt)
                .collect(toList());

        CombatGame game = new CombatGame();
        game.dealPlayer1(cardsP1);
        game.dealPlayer2(cardsP2);

        game.play();

        System.out.println("Part I  >>> " + game.getWinnersScore());
//end::mainPart1[]

//tag::mainPart2[]
        RecursiveCombatGame recursiveGame = new RecursiveCombatGame();
        recursiveGame.dealPlayer1(cardsP1);
        recursiveGame.dealPlayer2(cardsP2);

        recursiveGame.play();

        System.out.println("Part II >>> " + recursiveGame.getWinnersScore());
    }
//end::mainPart2[]
}

enum Player { ONE, TWO }

//tag::part1[]
class CombatGame {

    protected final Deque<Integer> deckP1 = new ArrayDeque<>();
    protected final Deque<Integer> deckP2 = new ArrayDeque<>();

    protected Player winner;
    protected int winnersScore;

    void dealPlayer1(Iterable<Integer> cards) {
        dealPlayer(cards, Player.ONE);
    }

    void dealPlayer2(Iterable<Integer> cards) {
        dealPlayer(cards, Player.TWO);
    }

    private void dealPlayer(Iterable<Integer> cards, Player player) {
        var deck = player == Player.ONE ? deckP1 : deckP2;
        deck.clear();
        for (Integer card : cards) {
            deck.addLast(card);
        }
    }

    public void play() {
        while (!(deckP1.isEmpty() || deckP2.isEmpty())) {
            playRound();
        }
        evaluateOutcome();
    }

    protected void playRound() {
        int cardP1 = deckP1.pop();
        int cardP2 = deckP2.pop();

        if (cardP1 > cardP2) {
            deckP1.addLast(cardP1);
            deckP1.addLast(cardP2);
        } else if (cardP2 > cardP1){
            deckP2.addLast(cardP2);
            deckP2.addLast(cardP1);
        }
    }

    protected void evaluateOutcome() {
        Deque<Integer> winnigDeck;
        if (deckP1.isEmpty()) {
            winner = Player.TWO;
            winnigDeck = deckP2;
        } else if (deckP2.isEmpty()) {
            winner = Player.ONE;
            winnigDeck = deckP1;
        } else {
            throw new IllegalStateException();
        }
        calculateWinnersScore(winnigDeck);
    }

    protected void calculateWinnersScore(Deque<Integer> winnigDeck) {
        int score = 0;
        int i = winnigDeck.size();
        for (int card : winnigDeck) {
            score += card * i--;
        }
        this.winnersScore = score;
    }

    public Player getWinner() {
        return winner;
    }

    public int getWinnersScore() {
        return winnersScore;
    }
}
//end::part1[]

//tag::part2[]
class RecursiveCombatGame extends CombatGame {

    private final Set<String> p1History = new HashSet<>();
    private final Set<String> p2History = new HashSet<>();

    @Override
    public void play() {
        boolean isHistoricDeck = false;
        while (deckP1.size() > 0 && deckP2.size() > 0) {
            String deckP1h = deckP1.toString();
            String deckP2h = deckP2.toString();
            if (isHistoricDeck(deckP1h, deckP2h)) {
                isHistoricDeck = true;
                break;
            }
            p1History.add(deckP1h);
            p2History.add(deckP2h);

            playRound();
        }
        if (isHistoricDeck) {
            winner = Player.ONE;
        } else {
            evaluateOutcome();
        }
    }

    private boolean isHistoricDeck(String deckP1, String deckP2) {
        return p1History.contains(deckP1) || p2History.contains(deckP2);
    }

    @Override
    protected void playRound() {
        int cardP1 = deckP1.pop();
        int cardP2 = deckP2.pop();

        if (deckP1.size() >= cardP1 && deckP2.size() >= cardP2) {
            RecursiveCombatGame subGame = new RecursiveCombatGame();
            subGame.dealPlayer1(deckP1, cardP1);
            subGame.dealPlayer2(deckP2, cardP2);
            subGame.play();

            if (subGame.getWinner() == Player.ONE) {
                deckP1.addLast(cardP1);
                deckP1.addLast(cardP2);
            } else if (subGame.getWinner() == Player.TWO) {
                deckP2.addLast(cardP2);
                deckP2.addLast(cardP1);
            }
        } else {
            if (cardP1 > cardP2) {
                deckP1.addLast(cardP1);
                deckP1.addLast(cardP2);
            } else if (cardP2 > cardP1){
                deckP2.addLast(cardP2);
                deckP2.addLast(cardP1);
            }
        }
    }

    private void dealPlayer1(Deque<Integer> deckP1, int numCardsP1) {
        dealPlayer(deckP1, numCardsP1, Player.ONE);
    }

    private void dealPlayer2(Deque<Integer> deckP2, int numCardsP2) {
        dealPlayer(deckP2, numCardsP2, Player.TWO);
    }

    private void dealPlayer(Deque<Integer> originalDeck, int numCards, Player player) {
        var deck = player == Player.ONE ? deckP1 : deckP2;
        deck.addAll(originalDeck);
        while (deck.size() > numCards) {
            deck.removeLast();
        }
    }
}
//end::part2[]
