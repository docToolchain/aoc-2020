import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

import static java.util.stream.Collectors.toList;

public class Day16 {

    private static final int FIELDS_COUNT = 20;

    public static void main(String[] args) throws IOException {
        // Part 1
        List<String> input = Files.readAllLines(Path.of("day16.txt"));

        List<Category> categories = parseCategories(input);
        int[][] nearbyTickets = parseTickets(input, true, categories);

        int invalidValuesSum = 0;
        for (int[] ticket : nearbyTickets) {
            invalidValuesSum += sumOfInvalidValues(ticket, categories);
        }
        System.out.println("Solution for Part I  >>> " + invalidValuesSum);

        // Part 2
        int[][] validTickets = parseTickets(input, false, categories);
        Map<Integer, List<Category>> allCandidates = new TreeMap<>();

        // collect candidates for each field
        for (int field = 0; field < FIELDS_COUNT; field++) {
            for (Category category : categories) {
                boolean isCandidateForField = true;
                for (int[] ticket : validTickets) {
                    if (!category.isInRange(ticket[field])) {
                        isCandidateForField = false;
                        break;
                    }
                }
                if (isCandidateForField) {
                    // add category to the field's list of candidates
                    allCandidates.computeIfAbsent(field, k -> new ArrayList<>()).add(category);
                }
            }
        }

        // Start with the field that has only one candidate.
        // Store the candidate and remove it from all other fields' candidate lists.
        // Fortunately there is one field with only one candidate after each iteration,
        // so we continue until each field has one category assigned to it
        Map<Integer, Category> fieldToCategory = new HashMap<>();
        while (fieldToCategory.size() < 20) {
            for (var candidatesEntry : allCandidates.entrySet()) {
                if (candidatesEntry.getValue().size() == 1) {
                    Category category = candidatesEntry.getValue().get(0);
                    fieldToCategory.put(candidatesEntry.getKey(), category);
                    allCandidates.values().forEach(l -> l.remove(category));
                    break;
                }
            }
        }
        System.out.println("Fields: " + fieldToCategory);

        int[] myTicket = new int[]{173, 191, 61, 199, 101, 179, 257, 79, 193, 223, 139, 97, 83, 197, 251, 53, 89, 149, 181, 59};

        // which fields' categories start with "departure"?
        int[] departureFields = fieldToCategory.entrySet().stream()
                .filter(e -> e.getValue().name.startsWith("departure"))
                .mapToInt(Map.Entry::getKey)
                .toArray();

        // calculate the solution
        long result = 1;
        for (int departureField : departureFields) {
            result *= myTicket[departureField];
        }

        System.out.println("Solution for Part II >>> " + result);
    }

    static List<Category> parseCategories(List<String> input) {
        return input.stream()
                .takeWhile(l -> !l.isBlank())
                .map(Category::parse)
                .collect(toList());
    }

    static int[][] parseTickets(List<String> input, boolean keepInvalid, List<Category> cat) {
        List<String> nearby = readNearbyTickets(input);
        return nearby.stream()
                .map(l -> toIntArray(l))
                .filter(t -> keepInvalid || isValid(t, cat))
                .toArray(int[][]::new);
    }

    private static boolean isValid(int[] ticket, List<Category> categories) {
        // valid if ticket has no invalid values
        return invalidValues(ticket, categories).size() == 0;
    }

    private static List<String> readNearbyTickets(List<String> input) {
        List<String> nearby = new ArrayList<>();
        boolean nearbyTickets = false;
        for (String line : input) {
            if (nearbyTickets) {
                nearby.add(line);
            } else if (line.startsWith("nearby tickets:")) {
                nearbyTickets = true;
            }
        }
        return nearby;
    }

    public static int sumOfInvalidValues(int[] ticket, List<Category> categories) {
        return invalidValues(ticket, categories).stream()
                .mapToInt(Integer::intValue)
                .sum();
    }

    private static int[] toIntArray(String line) {
        return Stream.of(line.split(","))
                .mapToInt(Integer::parseInt)
                .toArray();
    }

    public static List<Integer> invalidValues(int[] values, List<Category> categories) {
        List<Integer> invalidValues = new ArrayList<>();
        for (int val : values) {
            boolean inRange = false;
            for (Category category : categories) {
                if (category.isInRange(val)) {
                    inRange = true;
                }
            }
            if (!inRange) {
                invalidValues.add(val);
            }
        }
        return invalidValues;
    }
}

class Category {

    private static final Pattern PATTERN = Pattern.compile("(.+): (\\d+)-(\\d+) or (\\d+)-(\\d+)");

    String name;
    int range1Start, range1End, range2Start, range2End;

    static Category parse(String str) {
        Matcher m = PATTERN.matcher(str);
        if (!m.matches()) {
            throw new IllegalArgumentException("Invalid category string");
        }
        Category c = new Category();
        c.name = m.group(1);
        c.range1Start = Integer.parseInt(m.group(2));
        c.range1End = Integer.parseInt(m.group(3));
        c.range2Start = Integer.parseInt(m.group(4));
        c.range2End = Integer.parseInt(m.group(5));

        return c;
    }

    public boolean isInRange(int i) {
        return (i >= range1Start && i <= range1End) || (i >= range2Start && i <= range2End);
    }

    @Override
    public String toString() {
        // for debug output it's sufficient to print the name
        return name;
    }
}