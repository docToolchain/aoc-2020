ArrayList<String> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator")))
println("Solution Part 1: " + getMax(input))
println("Solution Part 2: " + getMissingSeat(input))

int getMax(ArrayList<String> input) {
    return input.collect( seat -> {
        getNumberFromSeatString(seat as String)
    }).max()
}

int getMin(ArrayList<String> input) {
    return input.collect( seat -> {
        getNumberFromSeatString(seat as String)
    }).min()
}

int getNumberFromSeatString(String seat) {
    return Integer.parseInt(seat.replace("B", "1").replace("F", "0").replace("R", "1").replace("L", "0"), 2)
}

int getMissingSeat(ArrayList<String> input) {
    ArrayList transform = input.collect( seat -> {
        getNumberFromSeatString(seat as String)
    })

    int missingSeat = 0
    for (int i = getMin(input); i <= getMax(input); i++){
        if (!transform.contains(i)){
            missingSeat = i
            break
        }
    }
    return missingSeat
}
