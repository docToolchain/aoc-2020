import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class Day18 {

    public static void main(String[] args) throws IOException {
//tag::part1main[]
        Day18 solver = new Day18();
        List<String> input = Files.readAllLines(Path.of("day18.txt"));

        long result = input.stream()
                .mapToLong(solver::evaluatePart1)
                .sum();

        System.out.println("Solution of Part I  >>> " + result);
//end::part1main[]

//tag::part2main[]
        result = input.stream()
                .mapToLong(solver::evaluatePart2)
                .sum();
        System.out.println("Solution of Part II >>> " + result);
//end::part2main[]
    }

//tag::part1[]
    public long evaluatePart1(String expression) {
        return evaluate(expression);
    }

    public long evaluate(String expression) {
        // remove spaces so that we don't have to deal with them in evaluation
        return eval(expression.replace(" ", ""));
    }

    private long eval(String expression) {
        long result = -1;
        char operator = 0;
        while (expression.length() > 0) {
            char symbol = expression.charAt(0);
            long val;
            if (symbol == '(') {
                String subExpression = getSubExpression(expression);
                val = eval(subExpression);
                result = calculate(operator, val, result);
                expression = expression.substring(subExpression.length()+2); // +2 to also remove parantheses
            } else {
                if (Character.isDigit(symbol)) {
                    val = Character.getNumericValue(symbol);
                    result = calculate(operator, val, result);
                } else if (symbol == '+' || symbol == '*') {
                    operator = symbol;
                }
                expression = expression.substring(1);
            }
        }
        return result;
    }

    private long calculate(char operation, long operand1, long operand2) {
        if (operation == 0) {
            return operand1;
        } else if (operation == '+') {
            return operand1 + operand2;
        } else if (operation == '*') {
            return operand1 * operand2;
        }
        throw new UnsupportedOperationException("'" + operation + "'");
    }

    String getSubExpression(String expression) {
        ensureStartsWithParanthesis(expression);
        int openParantheses = 1;
        for (int i = 1; i < expression.length(); i++) {
            if (expression.charAt(i) == ')') {
                openParantheses--;
            } else if (expression.charAt(i) == '(') {
                openParantheses++;
            }
            if (openParantheses == 0) {
                return expression.substring(1, i);
            }
        }

        throw new IllegalArgumentException("Matching closing paranthesis is missingin expression '" + expression + "'");
    }

    private void ensureStartsWithParanthesis(String expression) {
        if (!expression.startsWith("(")) {
            throw new IllegalArgumentException("expression must start with ( but was '" + expression + "'");
        }
    }
//end::part1[]

//tag::part2[]
    public long evaluatePart2(String expression) {
        return evaluate(addParanthesesAroundAdditions(expression));
    }

    String addParanthesesAroundAdditions(String expression) {
        StringBuilder sb = new StringBuilder(expression);

        int idx = sb.indexOf("+");
        while (idx > 0) {
            int openIdx = getOpenIdx(sb, idx);
            sb.insert(openIdx, "(");
            int closingIdx = getClosingIdx(sb, idx+1);
            sb.insert(closingIdx, ")");

            idx = sb.indexOf("+", idx+2);
        }
        return sb.toString();
    }

    private int getOpenIdx(StringBuilder sb, int idx) {
        char charAt = sb.charAt(idx - 2);
        if (Character.isDigit(charAt)) {
            return idx - 2;
        }
        int parantheses = 0;
        for (int i = idx - 2; i >= 0; i--) {
            if (sb.charAt(i) == ')') {
                parantheses++;
            } else if (sb.charAt(i) == '(') {
                parantheses--;
            }
            if (parantheses == 0) {
                return i;
            }
        }
        throw new IllegalArgumentException();
    }

    private int getClosingIdx(StringBuilder sb, int idx) {
        char charAt = sb.charAt(idx + 2);
        if (Character.isDigit(charAt)) {
            return idx + 3;
        }
        int parantheses = 0;
        for (int i = idx + 2; i < sb.length(); i++) {
            if (sb.charAt(i) == '(') {
                parantheses++;
            } else if (sb.charAt(i) == ')') {
                parantheses--;
            }
            if (parantheses == 0) {
                return i;
            }
        }
        throw new IllegalArgumentException();
    }
//end::part2[]
}
