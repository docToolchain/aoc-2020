#!/usr/bin/env groovy

ArrayList<String> inputNumbersAsString = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator")))
ArrayList<Integer> inputNumbers = new ArrayList<Integer>()
for(int i = 0; i < inputNumbersAsString.size(); i++)
{
   inputNumbers[i] = Integer.parseInt(inputNumbersAsString[i]);
}

println "\n"
part1(inputNumbers)
println "\n"
part2(inputNumbers)

void part1(ArrayList<Integer> inputNumbers) {
    // tag::loopsPart1[]
    for(int i = 0; i < inputNumbers.size(); i++) {
        for(int j = i + 1; j < inputNumbers.size(); j++) {
            int sum = inputNumbers[i] + inputNumbers[j]
    // end::loopsPart1[]
            if(sum == 2020) {
                int solution = inputNumbers[i] * inputNumbers[j]
                println "Solution Part 1:"
                println "   Num1: " + inputNumbers[i]
                println "   Num2: " + inputNumbers[j]
                println "   Solution: " + solution
            }
        }
    }
}

void part2(ArrayList<Integer> inputNumbers) {
    // tag::loopsPart2[]
    for(int i = 0; i < inputNumbers.size(); i++) {
        for(int j = i + 1; j < inputNumbers.size(); j++) {
            for(int k = j + 1; k < inputNumbers.size(); k++) {
                int sum = inputNumbers[i] + inputNumbers[j] + inputNumbers[k]
    // end::loopsPart2[]
                if(sum == 2020) {
                    int solution = inputNumbers[i] * inputNumbers[j] * inputNumbers[k]
                    println "Solution Part 2:"
                    println "   Num1: " + inputNumbers[i]
                    println "   Num2: " + inputNumbers[j]
                    println "   Num3: " + inputNumbers[k]
                    println "   Solution: " + solution
                }
            }
        }
    }
}
