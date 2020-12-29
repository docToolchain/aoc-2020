test()
solve()

void solve() {
    // tag::splitInput[]
    ArrayList<String> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator")))
    println("Solution Part 1: " + solvePart1(input))
    println("Solution Part 2: " + solvePart2(input))
    // end::splitInput[]
}

Long solvePart1(ArrayList<String> input) {
    // tag::solvePart1[]
    Long sum = 0
    input.forEach{String expression ->
        sum += solveExpressionPart1(expression)
    }
    return sum
    // end::solvePart1[]
}

Long solvePart2(ArrayList<String> input) {
    // tag::solvePart2[]
    Long sum = 0
    input.forEach{String expression ->
        sum += solveExpressionPart2(expression)
    }
    return sum
    // end::solvePart2[]
}

String removeBracesPart1(String expression) {
    while(expression.indexOf("(") != -1) {
        int indexClosingBraces = expression.indexOf(")")
        int indexOpeningBraces = expression.substring(0, indexClosingBraces).lastIndexOf("(")
        String subExpression = expression.substring(indexOpeningBraces + 1, indexClosingBraces)
        Long subExpressionSolition = solveExpressionPart1(subExpression)
        String expressionBeforeBraces = expression.substring(0, indexOpeningBraces)
        String expressionAfterBraces = expression.substring(indexClosingBraces + 1, expression.length())
        expression = expressionBeforeBraces + subExpressionSolition.toString() + expressionAfterBraces
    }
    return expression
}

Long solveExpressionPart1(String expression) {
    expression = removeBracesPart1(expression)
    while(expression.indexOf(" ") != -1) {
        int index = expression.indexOf(" ")
        Long n1 = Long.parseLong(expression.substring(0, index))
        expression = expression.substring(index + 1, expression.length())

        index = expression.indexOf(" ")
        String operator = expression.substring(0, index)
        expression = expression.substring(index + 1, expression.length())

        index = expression.indexOf(" ")
        if(index == -1) index = expression.length()
        Long n2 = Long.parseLong(expression.substring(0, index))
        expression = expression.substring(index, expression.length())

        Long solution = calc(n1, n2, operator)
        expression = solution + expression
    }
    return Long.parseLong(expression)
}

String removeBracesPart2(String expression) {
    while(expression.indexOf("(") != -1) {
        int indexClosingBraces = expression.indexOf(")")
        int indexOpeningBraces = expression.substring(0, indexClosingBraces).lastIndexOf("(")
        String subExpression = expression.substring(indexOpeningBraces + 1, indexClosingBraces)
        Long subExpressionSolition = solveExpressionPart2(subExpression)
        String expressionBeforeBraces = expression.substring(0, indexOpeningBraces)
        String expressionAfterBraces = expression.substring(indexClosingBraces + 1, expression.length())
        expression = expressionBeforeBraces + subExpressionSolition.toString() + expressionAfterBraces
    }
    return expression
}

Long solveExpressionPart2(String expression) {
    expression = removeBracesPart2(expression)
    while(expression.indexOf(" ") != -1) {
        if(expression.indexOf("+") != -1) {
            int index = expression.indexOf("+")

            String expressionBeforePlus = expression.substring(0, index - 1)
            int indexSpaceBeforePlus = expressionBeforePlus.lastIndexOf(" ")
            Long n1 = Long.parseLong(expressionBeforePlus.substring(indexSpaceBeforePlus + 1, expressionBeforePlus.length()))

            String expressionAfterPlus = expression.substring(index + 2, expression.length())
            int indexSpaceAfterPlus = expressionAfterPlus.indexOf(" ")
            indexSpaceAfterPlus = indexSpaceAfterPlus == -1 ? expressionAfterPlus.length() : indexSpaceAfterPlus
            Long n2 = Long.parseLong(expressionAfterPlus.substring(0, indexSpaceAfterPlus))

            Long solution = calc(n1, n2, "+")

            expressionBeforePlus = expressionBeforePlus.substring(0, indexSpaceBeforePlus + 1)
            expressionAfterPlus = expressionAfterPlus.substring(indexSpaceAfterPlus, expressionAfterPlus.length())
            expression = expressionBeforePlus + solution + expressionAfterPlus
        } else {
            int index = expression.indexOf(" ")
            Long n1 = Long.parseLong(expression.substring(0, index))
            expression = expression.substring(index + 1, expression.length())

            index = expression.indexOf(" ")
            String operator = expression.substring(0, index)
            expression = expression.substring(index + 1, expression.length())

            index = expression.indexOf(" ")
            if(index == -1) index = expression.length()
            Long n2 = Long.parseLong(expression.substring(0, index))
            expression = expression.substring(index, expression.length())

            Long solution = calc(n1, n2, operator)
            expression = solution + expression
        }
    }
    return Long.parseLong(expression)
}

Long calc(Long n1, Long n2, String operator) {
    Long solution
    switch (operator) {
        case "+":
            solution = n1 + n2
            break
        case "*":
            solution = n1 * n2
            break
        default:
            throw new Exception("FAIL")
    }
    return solution
}

void test() {
    ArrayList<String> input = Arrays.asList(new File("input_test_1.txt").text.split(System.getProperty("line.separator")))
    assert removeBracesPart1(input[0]) == "2 * 3 + 20"

    assert solveExpressionPart1(input[0]) == 26
    assert solveExpressionPart1(input[1]) == 437
    assert solveExpressionPart1(input[2]) == 12240
    assert solveExpressionPart1(input[3]) == 13632
    assert solvePart1(input) == 26335

    assert solveExpressionPart2(input[0]) == 46
    assert solveExpressionPart2(input[1]) == 1445
    assert solveExpressionPart2(input[2]) == 669060
    assert solveExpressionPart2(input[3]) == 23340
    assert solvePart2(input) == 693891
}
