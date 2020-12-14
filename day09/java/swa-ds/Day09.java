import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class Day09 {

    public static void main(String[] args) throws IOException {
        long[] numbers = Files.readAllLines(Path.of("day09.txt")).stream()
                .mapToLong(Long::parseLong)
                .toArray();

        // Part 1
        XmasVerifier xmasVerifier = new XmasVerifier(25);
        long validNumbers = xmasVerifier.findFirstInvalid(numbers);
        System.out.println(validNumbers);

        // Part 2
        int firstInvalidIdx = xmasVerifier.indexOfFirstInvalid(numbers);
        long weakness = xmasVerifier.findWeakness(firstInvalidIdx, numbers);

        System.out.println(weakness);
    }

}

class XmasVerifier {

    private final int preamble;

    XmasVerifier(int preamble) {
        this.preamble = preamble;
    }

    long findFirstInvalid(long... numbers) {
        int firstInvalidIdx = indexOfFirstInvalid(numbers);
        return numbers[firstInvalidIdx];
    }

    int indexOfFirstInvalid(long... numbers) {
        for (int idx = preamble; idx < numbers.length; idx++) {
            long numToVerify = numbers[idx];
            if (!isValid(numToVerify, idx, numbers)) {
                return idx;
            }
        }

        throw new IllegalStateException("No invalid number found!");
    }

    private boolean isValid(long numToVerify, int idx, long[] numbers) {
        for (int i = idx - preamble; i < idx; i++) {
            for (int j = i + 1; j < idx; j++) {
                long a = numbers[i];
                long b = numbers[j];
                if (a + b == numToVerify && a != b) {
                    return true;
                }
            }
        }
        return false;
    }

    public long findWeakness(int firstInvalidIdx, long[] numbers) {
        long firstInvalid = numbers[firstInvalidIdx];
        for (int i = 0; i < firstInvalidIdx; i++) {
            for (int j = i + 1; j < firstInvalidIdx; j++) {
                long sum = sumOf(numbers, i, j);
                if (sum == firstInvalid) {
                    return min(numbers, i, j) + max(numbers, i, j);
                }
            }
        }
        throw new IllegalStateException("Could not find weakness!");
    }

    private long max(long[] numbers, int startIdx, int endIdx) {
        long max = Long.MIN_VALUE;
        for (int i = startIdx; i < endIdx; i++) {
            max = Math.max(max, numbers[i]);
        }
        return max;
    }

    private long min(long[] numbers, int startIdx, int endIdx) {
        long min = Long.MAX_VALUE;
        for (int i = startIdx; i < endIdx; i++) {
            min = Math.min(min, numbers[i]);
        }
        return min;
    }

    private long sumOf(long[] numbers, int startIdx, int endIdx) {
        long sum = 0;
        for (int i = startIdx; i < endIdx; i++) {
            sum += numbers[i];
        }
        return sum;
    }

}
