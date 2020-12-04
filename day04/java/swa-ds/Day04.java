import static java.util.stream.Collectors.toMap;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Predicate;
import java.util.regex.Pattern;
import java.util.stream.Stream;

public class Day04 {

//tag::parsePassports[]
    public List<Passport> parsePassports(String passportFile) throws IOException {
        List<String> lines = Files.readAllLines(Path.of("day04.txt"));
        StringBuilder sb = new StringBuilder();
        List<Passport> passports = new ArrayList<>(lines.size());
        for (int i=0; i<lines.size(); i++) {
            String line = lines.get(i);
            if (!line.isBlank() || i == lines.size()-1) {
                sb.append(line).append(" ");
            } else {
                passports.add(new Passport(sb.toString()));
                sb = new StringBuilder();
            }
        }
        passports.add(new Passport(sb.toString()));

        return passports;
    }
//end::parsePassports[]

    public long countValidPassports(List<Passport> passports, Predicate<Passport> validFunction) {
        return passports.stream()
                .filter(validFunction)
                .count();
    }

    public static void main(String[] args) throws IOException {
//tag::part1[]
        Day04 solver = new Day04();

        List<Passport> passports = solver.parsePassports("/day04.txt"); // <1>

        long solutionPart1 = solver.countValidPassports(passports, Passport::isValidPart1); // <2>
        System.out.println(solutionPart1);
//end::part1[]

        long solutionPart2 = solver.countValidPassports(passports, Passport::isValidPart2);
        System.out.println(solutionPart2);
    }
}

class Passport {

//tag::initPassport[]
    private final Map<String, String> passportData;

    public Passport(String passportString) {
        passportData = Stream.of(passportString.split(" "))
                .map(passportEntry -> passportEntry.split(":"))
                .collect(toMap(attribute -> attribute[0], a -> a[1]));
    }
//end::initPassport[]

//tag::isValidPart1[]
    boolean isValidPart1() {
        return (passportData.size() == 8 || (passportData.size() == 7 && !passportData.containsKey("cid") ));
    }
//end::isValidPart1[]

//tag::isValidPart2[]
    boolean isValidPart2() {
        return isValidYear("byr", 1920, 2002)
                && isValidYear("iyr", 2010, 2020)
                && isValidYear("eyr", 2020, 2030)
                && isValidHeight()
                && isValidHairColor()
                && isValidEyeColor()
                && isValidPassportId();
    }

    private boolean isValidYear(String attributeKey, int from, int to) {
        if (!passportData.containsKey(attributeKey)) {
            return false;
        }
        int year = Integer.parseInt(passportData.get(attributeKey));
        return year >= from && year <= to;
    }

    private boolean isValidHeight() {
        if (!passportData.containsKey("hgt")) {
            return false;
        }
        String hgtStr = passportData.get("hgt");
        int min, max;
        String measureUnit = hgtStr.substring(hgtStr.length() - 2);
        if (measureUnit.equals("in")) {
            min = 59;
            max = 76;
        } else if (measureUnit.equals("cm")) {
            min = 150;
            max = 193;
        } else {
            return false;
        }
        hgtStr = hgtStr.substring(0, hgtStr.length() - 2);
        int height = Integer.parseInt(hgtStr);
        return height >= min && height <= max;
    }

    private static final Pattern HAIR_COLOR_PATTERN = Pattern.compile("#[0-9a-f]{6}");

    private boolean isValidHairColor() {
        String hcl = passportData.get("hcl");
        return hcl != null && HAIR_COLOR_PATTERN.matcher(hcl).matches();
    }

    private static final Set<String> VALID_EYE_COLORS = Set.of("amb", "blu", "brn", "gry", "grn", "hzl", "oth");

    private boolean isValidEyeColor() {
        String ecl = passportData.get("ecl");
        return ecl != null && VALID_EYE_COLORS.contains(ecl);
    }

    private static final Pattern PASSPORT_ID_PATTERN = Pattern.compile("[0-9]{9}");

    private boolean isValidPassportId() {
        String pid = passportData.get("pid");
        return pid != null && PASSPORT_ID_PATTERN.matcher(pid).matches();
    }
//end::isValidPart2[]
    @Override
    public String toString() {
        return "Passport{" + passportData + "}";
    }

}

