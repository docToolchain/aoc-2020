// tag::splitInput[]
ArrayList<String> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator")))
// end::splitInput[]
println("Solution Part 1: " + getMax(input))
println("Solution Part 2: " + getMissingSeat(input))

int getMax(ArrayList<String> input) {
    // tag::getMax[]
    return input.collect( seat -> {
        getNumberFromSeatString(seat as String)
    }).max()
    // end::getMax[]
}

int getMin(ArrayList<String> input) {
    return input.collect( seat -> {
        getNumberFromSeatString(seat as String)
    }).min()
}

int getNumberFromSeatString(String seat) {
    // tag::getNumberFromSeatString[]
    return Integer.parseInt(seat.replace("B", "1").replace("F", "0").replace("R", "1").replace("L", "0"), 2)
    // end::getNumberFromSeatString[]
}

int getMissingSeat(ArrayList<String> input) {
    // tag::getMissingSeatTransform[]
    ArrayList seatList = input.collect( seat -> {
        getNumberFromSeatString(seat as String)
    })
    // end::getMissingSeatTransform[]

    // tag::getMissingSeat[]
    int missingSeat = 0
    for (int i = getMin(input); i <= getMax(input); i++){
        if (!seatList.contains(i)){
            missingSeat = i
            break
        }
    }
    return missingSeat
    // end::getMissingSeat[]
}
