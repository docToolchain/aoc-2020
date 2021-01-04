import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.List;
import java.util.Map;
import java.util.function.BiFunction;

public class Day18_ShuntingYard {

    public static void main(String[] args) throws IOException {
        List<String> input = Files.readAllLines(Path.of("day18.txt"));

        // Part 1
        Map<Character, Integer> precedencesPart1 = Map.of('+', 1, '*', 1);
        var rpn1 = new ReversePolishNotation(precedencesPart1);

        long result = input.stream()
                .mapToLong(expr -> {
                    rpn1.parse(expr);
                    return rpn1.evaluate();
                })
                .sum();
        System.out.println("Solution of Part I  >>> " + result);

        // Part 2
        Map<Character, Integer>precedencesPart2 = Map.of('+', 2, '*', 1);
        var rpn2 = new ReversePolishNotation(precedencesPart2);

        result = input.stream()
                .mapToLong(expr -> {
                    rpn2.parse(expr);
                    return rpn2.evaluate();
                })
                .sum();
        System.out.println("Solution of Part II >>> " + result);
    }

}

class ReversePolishNotation {

    private final Map<Character, Integer> precedences;
    private final Map<Character, BiFunction<Long, Long, Long>> operations = Map.of(
            '+', (a, b) -> a + b,
            '*', (a, b) -> a * b
    );

    String rpn;

    ReversePolishNotation(Map<Character, Integer> precedences) {
        this.precedences = precedences;
    }

    // create reverse polish notation (rpn) using the shunting yard algorithm
    void parse(String infixExpression) {
        Deque<Character> opStack = new ArrayDeque<>();
        StringBuilder rpnBuilder = new StringBuilder();
        for (char symbol : infixExpression.toCharArray()) {
            if (Character.isDigit(symbol)) {
                rpnBuilder.append(symbol).append(' ');
            } else if (isOperator(symbol)) {
                while (opStack.size() > 0 && precedenceOf(opStack.peek()) >= precedenceOf(symbol)) {
                    rpnBuilder.append(opStack.pop()).append(' ');
                }
                opStack.push(symbol);
            } else if (symbol == '(') {
                opStack.push(symbol);
            } else if (symbol == ')') {
                char op;
                while ((op = opStack.pop()) != '(') {
                    rpnBuilder.append(op).append(' ');
                }
            }
        }
        while (opStack.size() > 1) {
            rpnBuilder.append(opStack.pop()).append(' ');
        }
        rpnBuilder.append(opStack.pop());

        this.rpn = rpnBuilder.toString();
    }

    private int precedenceOf(Character symbol) {
        return precedences.getOrDefault(symbol, -1);
    }

    private boolean isOperator(char symbol) {
        return symbol == '+' || symbol == '*';
    }

    public String getRpn() {
        return rpn;
    }

    // evaluate the rpn
    public long evaluate() {
        Deque<Long> stack = new ArrayDeque<>(rpn.length());
        for (char symbol : rpn.toCharArray()) {
            if (Character.isDigit(symbol)) {
                stack.push((long) Character.getNumericValue(symbol));
            } else if (isOperator(symbol)) {
                long b = stack.pop();
                long a = stack.pop();
                stack.push(calculate(symbol, a, b));
            }
        }
        return stack.pop();
    }

    private long calculate(char symbol, long a, long b) {
        return operations.get(symbol).apply(a, b);
    }
}