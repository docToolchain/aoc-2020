test()
solve()

void solve() {
    // tag::splitInput[]
    ArrayList<String> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator")))
    // end::splitInput[]
    println("Solution Part 1: " + solvePart1(input))
    println("Solution Part 2: " + solvePart2(input))
}

int solvePart1(ArrayList<String> input) {
    return executeProgram(input)[1]
}

int solvePart2(ArrayList<String> input) {
    Tuple terminationState
    // tag::solvePart2[]
    for(int i = 0; i < input.size(); i++) {
        ArrayList modifiedInput = deepcopy(input)
        if(modifiedInput[i].startsWith("jmp")) {
            modifiedInput[i] = modifiedInput[i].replace("jmp", "nop")
        }
        else if(modifiedInput[i].startsWith("nop")) {
            modifiedInput[i] = modifiedInput[i].replace("nop", "jmp")
        }
        terminationState = executeProgram(modifiedInput)
        if(terminationState[0] == true) {
            break
        }
    }
    // end::solvePart2[]
    return terminationState[1]
}

Tuple executeProgram(ArrayList<String> input) {
    ArrayList<Integer> executedCommands = new ArrayList<>()
    Boolean successfulExecution = true
    int position = 0
    int accumulator = 0
    // tag::executeProgramExecutedCommands[]
    while (true) {
        if(executedCommands.contains(position)) {
            successfulExecution = false
            break
        }
        executedCommands.add(position)
    // end::executeProgramExecutedCommands[]
        if(position >= input.size()) {
            break
        }
        String command = input[position].substring(0,3)
        Integer number = Integer.parseInt(input[position].substring(4,input[position].length()))
        switch (command){
            case "acc":
                accumulator = accumulator + number
                position++
                break
            case "jmp":
                position = position + number
                break
            case "nop":
                position++
                break
            default:
                throw new Exception("FAIL")
        }

    }
    return new Tuple(successfulExecution, accumulator)
}

void test() {
    ArrayList<String> input = Arrays.asList(new File('input_test.txt').text.split(System.getProperty("line.separator")))
    assert solvePart1(input) == 5
    assert solvePart2(input) == 8
}

// standard deep copy implementation
def deepcopy(orig) {
    bos = new ByteArrayOutputStream()
    oos = new ObjectOutputStream(bos)
    oos.writeObject(orig); oos.flush()
    bin = new ByteArrayInputStream(bos.toByteArray())
    ois = new ObjectInputStream(bin)
    return ois.readObject()
}