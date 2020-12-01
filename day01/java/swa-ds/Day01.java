import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Day01 {


    public static int solvePart1(int... entries) {
        for (int i : entries) {
            for (int j : entries) {
                if (i + j == 2020) {
                    return i * j;
                }
            }
        }
        return -1;
    }

    public static int solvePart2(int... entries) {
        for (int i : entries) {
            for (int j : entries) {
                for (int k : entries) {
                    if (i + j + k == 2020) {
                        return i * j * k;
                    }
                }
            }
        }
        return -1;
    }

    public static void main(String[] args) throws IOException {
        int[] input = Files.lines(Paths.get("day01.txt"))
                .mapToInt(Integer::parseInt)
                .toArray();

        System.out.println(solvePart1(input));
        System.out.println(solvePart2(input));
    }

}
