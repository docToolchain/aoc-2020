import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.TreeSet;

public class Day05 {
//tag::decode[]

    enum Half { // <1>

        LOWER, HIGHER;

        static Half of(char c) { // <2>
            if (c == 'F' || c == 'L') {
                return LOWER;
            }
            if (c == 'B' || c == 'R') {
                return HIGHER;
            }
            throw new IllegalArgumentException();
        }
    }

    private int decode(String code, int low, int high) { // <3>
        for (int i = 0; i < code.length(); i++) {
            char c = code.charAt(i);
            Half half = Half.of(c);
            int difference = high - low;
            if (difference == 1) {
                return half == Half.LOWER ? low : high;
            }
            if (half == Half.LOWER) {
                high = high - (difference + 1) / 2;
            } else {
                low = low + (difference + 1) / 2;
            }
        }
        throw new IllegalStateException("This line should never be reached. If it does, it's a programming error!");
    }
//end::decode[]


//tag::decodeSeatId[]
    public int decodeSeatId(String seat) {
        String rowPart = seat.substring(0, 7);
        String columnPart = seat.substring(7);

        int row = decode(rowPart, 0, 127);
        int column = decode(columnPart, 0, 7);

        return row * 8 + column;
    }
//end::decodeSeatId[]

    public static void main(String[] args) throws IOException {
        List<String> lines = Files.readAllLines(Path.of("day05.txt"));
        Day05 solver = new Day05();

//tag::part1[]
        Optional<Integer> max = lines.stream()
                .map(solver::decodeSeatId) // <1>
                .max(Comparator.naturalOrder()); // <2>
        System.out.println("First star: " + max.orElseThrow()); // <3>
//end::part1[]

//tag::part2[]
        TreeSet<Integer> allSeatIds = lines.stream()
                .map(solver::decodeSeatId)
                .collect(TreeSet::new, TreeSet::add, TreeSet::addAll); // <1>

        int lowestSeatId = allSeatIds.first();
        int highestSeatId = allSeatIds.last();

        for (int i = lowestSeatId; i <= highestSeatId; i++) {
            if (!allSeatIds.contains(i)) {
                System.out.println("Second star:" + i);
            }
        }
//end::part2[]
    }


}
