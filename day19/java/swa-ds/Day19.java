import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;

import static java.util.stream.Collectors.toList;
import static java.util.stream.Collectors.toMap;

public class Day19 {
//tag::main[]
    public static void main(String[] args) throws IOException {
        // Read and parse input
        List<String> input = Files.readAllLines(Path.of("day19.txt"));

        var rules = input.stream()
                .takeWhile(l -> !l.isBlank())
                .collect(toList());

        var messages = input.stream()
                .skip(rules.size() + 1) // skip rules and empty line
                .collect(toList());

        // Part 1
        var msgValidator = new MessageValidator(rules, Part.ONE);

        long result = messages.stream()
                .filter(msgValidator::isValidMessage)
                .count();

        System.out.println("Solution of Part I  >>> " + result);

        // Part 2
        msgValidator = new MessageValidator(rules, Part.TWO);
        result = messages.stream()
                .filter(msgValidator::isValidMessage)
                .count();

        System.out.println("Solution of Part II >>> " + result);
    }
}

enum Part { ONE, TWO }
//end::main[]

//tag::msgValidator[]
class MessageValidator {

    private static final String DOUBLE_QUOTES = "\"";

    private final List<Pattern> ruleRegexList = new LinkedList<>();

    private Map<String, String> rules;
    private Map<String, String> letters;

    public MessageValidator(List<String> rules, Part part) {
        buildRules(rules, part);
    }

    private String extractKey(String rule) {
        return rule.substring(0, rule.indexOf(':'));
    }

    private String extractValue(String rule) {
        return rule.substring(rule.indexOf(": ") + 2);
    }

    public boolean isValidMessage(String msg) {
        for (Pattern regex : ruleRegexList) {
            if (regex.matcher(msg).matches()) {
                return true;
            }
        }
        return false;
    }

    private void buildRules(List<String> rules, Part part) {
        // map for the "letter" rules ("121" => "a"; "96" => "b")
        this.letters = new HashMap<>();
        // collect other rules in a map where the key represents the rule number
        // e.g.: "0" => "8 11"; "45": "96 48 | 121 131"; ...
        this.rules = rules.stream()
                .peek(line -> {
                    int idx = line.indexOf('"');
                    if (idx > 0) {
                        letters.put(line.substring(0, idx-2), line.substring(idx+1, idx+2));
                    }
                })
                .filter(l -> !l.contains(DOUBLE_QUOTES))
                .collect(toMap(this::extractKey, this::extractValue));
        if (part == Part.ONE) {
            String rule0 = this.rules.get("0");
            String ruleString = resolve(rule0);
            // list is needed for part 2; for part 1 we only add 1 regex
            ruleRegexList.add(Pattern.compile(ruleString));

        } else if (part == Part.TWO) {
//tag::examples[]
            // 0:  8 11
            // 8:  42 | 42 8
            // 11: 42 31 | 42 11 31
            // Examples:
            // =>  8: 42; 42 42; 42 42 42; ... => 42{1,}
            // => 11: 42 31; 42 42 31 31; 42 42 42 42 31 31 31 31 => 42{n}31{n}
            // => 0: 8 11: 42{1,}42{n}31{n} => 42{n+1,}31{n}
//end::examples[]
            String rule31 = resolve("31");
            String rule42 = resolve("42");

            for (int n = 1; n <= 4; n++) {
                // rule42{n+1,}rule31{n}
                String regex = String.format("%s{%d,}%s{%d}", rule42, n+1, rule31, n);
                ruleRegexList.add(Pattern.compile(regex));
            }

        } else {
            throw new IllegalArgumentException("No such part " + part + "!");
        }
    }

    private String resolve(String rule) {
        StringBuilder sb = new StringBuilder();
        String[] parts = rule.split(" ");
        boolean hasOr = false;
        for (String r : parts) {
            String letter = letters.get(r);
            if (letter != null) {
                sb.append(letter);
            } else if ("|".equals(r)) {
                sb.append("|");
                hasOr = true;
            } else {
                String rl = rules.get(r);
                if (rl != null) {
                    sb.append(resolve(rl)); // recursion
                }
            }
        }
        if (hasOr) {
            sb.insert(0, '(');
            sb.append(')');
        }
        return sb.toString();
    }
//end::msgValidator[]
}

