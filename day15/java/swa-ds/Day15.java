import java.time.Duration;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

public class Day15 {

//tag::part1[]
    private int[] startingNumbers;


    public void setStartingNumbers(int... numbers) {
        this.startingNumbers = numbers;
    }

    public int nthNumberSpoken1(int n) {
        int[] numbers = new int[n];
        System.arraycopy(startingNumbers, 0, numbers, 0, startingNumbers.length);

        int turn = startingNumbers.length - 1;
        while (turn < numbers.length - 1) {
            int lastSpokenNumber = numbers[turn];
            int spokenBeforeInTurn = turn;
            do {
                spokenBeforeInTurn--;
            } while (spokenBeforeInTurn >= 0 && numbers[spokenBeforeInTurn] != lastSpokenNumber);
            int nextNum;
            if (spokenBeforeInTurn == -1) {
                nextNum = 0;
            } else {
                nextNum = turn - spokenBeforeInTurn;
            }
            numbers[++turn] = nextNum;
        }
        return numbers[numbers.length - 1];
    }
//end::part1[]

//tag::part2[]
    public int nthNumberSpoken2(int n) {
        Map<Integer, Integer> lastSpokenInTurn = new HashMap<>();

        int lastNumber = -1;
        for (int turn = 1; turn <= n; turn++) {
            int previousTurn = turn - 1;
            if (turn <= startingNumbers.length) {
                if (turn > 1) {
                    lastSpokenInTurn.put(lastNumber, previousTurn);
                }
                lastNumber = startingNumbers[previousTurn];

            } else {
                int currentNumber =
                        lastSpokenInTurn.containsKey(lastNumber) ? (previousTurn - lastSpokenInTurn.get(lastNumber)) : 0;
                lastSpokenInTurn.put(lastNumber, previousTurn);
                lastNumber = currentNumber;
            }
        }

        return lastNumber;
    }
//end::part2[]

    public static void main(String[] args) {

//tag::mainPart1[]
        Day15 solver = new Day15();
        solver.setStartingNumbers(12, 20, 0, 6, 1, 17, 7);

        // Part 1
        int result = solver.nthNumberSpoken1(2020);
        System.out.println(result);
//end::mainPart1[]

        // Part 2
        Instant start = Instant.now();

//tag::mainPart2[]
        result = solver.nthNumberSpoken2(30_000_000);
        System.out.println(result);
//end::mainPart2[]

        Duration dur = Duration.between(start, Instant.now());
        System.out.println("Duration of Part 2: " + dur.toMinutesPart() + "min " + dur.toSecondsPart() + "s " + dur.toMillisPart() + "ms");
    }

}
