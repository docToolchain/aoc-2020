import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static java.util.stream.Collectors.toList;

public class Day10 {

    public static int solvePart1(List<String> input) {
        var adapters = input.stream()
                .map(Integer::valueOf)
                .sorted()
                .collect(toList());

        int joltage = 0;
        Map<Integer, Integer> differences = new HashMap<>();
        for (int adapter : adapters) {
            int diff = adapter - joltage;
            differences.putIfAbsent(diff, 0);
            differences.put(diff, differences.get(diff) + 1);
            joltage = adapter;
        }
        // difference to built-in adapter of device:
        differences.put(3, differences.get(3) + 1);

        System.out.println(differences);

        return differences.get(1) * differences.get(3);
    }

    public static void main(String[] args) throws IOException {
        List<String> input = Files.readAllLines(Path.of("day10.txt"));
        int solutionPart1 = Day10.solvePart1(input);
        System.out.println(solutionPart1);
    }

}
