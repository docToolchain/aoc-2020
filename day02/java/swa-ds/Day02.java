import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class Day02 {

//tag::part1[]
    public boolean isValidPasswordPart1(String password) {
        int hyphenIdx = password.indexOf('-'); // <1>
        int firstSpaceIdx = password.indexOf(' ');

        int minOccurs = Integer.parseInt(password.substring(0, hyphenIdx));
        int maxOccurs = Integer.parseInt(password.substring(hyphenIdx + 1, firstSpaceIdx));

        char c = password.charAt(firstSpaceIdx + 1);

        String pwd = password.substring(password.indexOf(':') + 1).trim(); // <2>

        long count = pwd.chars().filter(i -> i == c).count(); // <3>

        return count >= minOccurs && count <= maxOccurs; // <4>
    }
//end::part1[]

//tag::part2[]
    public boolean isValidPasswordPart2(String password) {
        int hyphenIdx = password.indexOf('-'); // <1>
        int firstSpaceIdx = password.indexOf(' ');

        int pos1 = Integer.parseInt(password.substring(0, hyphenIdx)) - 1;
        int pos2 = Integer.parseInt(password.substring(hyphenIdx + 1, firstSpaceIdx)) - 1;

        char c = password.charAt(firstSpaceIdx + 1);

        String pwd = password.substring(password.indexOf(':') + 1).trim(); // <2>

        int count = 0; // <3>
        if (pwd.charAt(pos1) == c) count++;
        if (pwd.charAt(pos2) == c) count++;

        return (count == 1); // <4>
    }
//end::part2[]

    public static void main(String[] args) throws IOException {
        Day02 solver = new Day02();

//tag::part1Eval[]
        List<String> passwordList = Files.readAllLines(Paths.get("day02.txt")); // <1>

        long validPasswords = passwordList.stream()
                .filter(solver::isValidPasswordPart1) // <2>
                .count();

        System.out.println("Part I - number of valid passwords: " + validPasswords);
//end::part1Eval[]

//tag::part2Eval[]
        validPasswords = passwordList.stream()
                .filter(solver::isValidPasswordPart2)
                .count();

        System.out.println("Part II - number of valid passwords: " + validPasswords);
//end::part2Eval[]
    }

}
