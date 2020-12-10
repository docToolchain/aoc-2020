import static java.util.stream.Collectors.toSet;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Day06 {

//tag::part1[]
    public long countAnswersPart1(List<String> input) {
        String inputCsv = String.join("~", input);

        String[] groups = inputCsv.split("~~");

        return Stream.of(groups)
                .mapToLong(group -> group.chars()
                        .filter(Character::isLetter)
                        .distinct()
                        .count())
                .sum();
    }
//end::part1[]

//tag::part2[]
    public long countAnswersPart2(List<String> input) {
        String inputCsv = String.join("~", input);
        String[] groups = inputCsv.split("~~");
        int count = 0;

        for (String group : groups) {
            List<String> answersPerPerson = Stream.of(group.split("~"))
                    .collect(Collectors.toList());
            // create set with "yes" answers of first person in group
            Set<Character> commonAnswers = new HashSet<>();
            commonAnswers.addAll(split(answersPerPerson.get(0)));
            // remove all "yes" answers from the set if not contained in any of the ohter group member's answers
            for (int i = 1; i < answersPerPerson.size(); i++) {
                Set<Character> splitAnswers = split(answersPerPerson.get(i));
                commonAnswers.removeIf(c -> !splitAnswers.contains(c));
            }
            count += commonAnswers.size();
        }
        return count;
    }
//end::part2[]

    private Set<Character> split(String answers) {
        return answers.chars().mapToObj(i -> (char) i).collect(toSet());
    }

    public static void main(String[] args) throws IOException {
        Day06 solver = new Day06();
//tag::main[]
        // Part 1
        List<String> input = Files.readAllLines(Path.of("day06.txt"));
        System.out.println(solver.countAnswersPart1(input));

        // Part 2
        System.out.println(solver.countAnswersPart2(input));
//end::main[]
    }

}
