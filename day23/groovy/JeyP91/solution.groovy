testPart1()
testPart2()
solve()

static void solve() {
    // tag::splitInput[]
    ArrayList<Integer> input = "523764819".split("").collect{Integer.parseInt(it)}
    println("Solution Part 1: " + solvePart1(input, 100))
    println("Solution Part 2: " + solvePart2(input, 10000000, 1000000))
    // end::splitInput[]
}

static Long solvePart1(ArrayList<Integer> input, int moves) {
    // tag::solvePart1[]
    Cups cups = new Cups()
    input.forEach{
        cups.add(it)
    }

    for(int i = 0; i < moves; i++) cups.performMove()

    return cups.displayPart1()
    // end::solvePart1[]
}

static Long solvePart2(ArrayList<Integer> input, int moves, int cupSize) {
    // tag::solvePart2[]
    Cups cups = new Cups()
    input.forEach{
        cups.add(it)
    }

    // Add additional cups
    for (int i = input.size() + 1; i <= cupSize; i++) cups.add(i)

    for(int i = 0; i < moves; i++) cups.performMove()

    return cups.displayPart2()
    // end::solvePart2[]
}

static void testPart1() {
    ArrayList<Integer> input = "389125467".split("").collect{Integer.parseInt(it)}
    Cups cups = new Cups()
    input.forEach{
        cups.add(it)
    }

    cups.performMove()
    assert cups.display() == "3  2  8  9  1  5  4  6  7"
    cups.performMove()
    assert cups.display() == "3  2  5  4  6  7  8  9  1"
    cups.performMove()
    assert cups.display() == "3  4  6  7  2  5  8  9  1"
    cups.performMove()
    assert cups.display() == "3  2  5  8  4  6  7  9  1"
    cups.performMove()
    assert cups.display() == "3  6  7  9  2  5  8  4  1"
    cups.performMove()
    assert cups.display() == "3  6  7  2  5  8  4  1  9"
    cups.performMove()
    assert cups.display() == "3  6  7  4  1  9  2  5  8"

    input = "389125467".split("").collect{Integer.parseInt(it)}
    assert solvePart1(input, 10) == 92658374

    input = "389125467".split("").collect{Integer.parseInt(it)}
    assert solvePart1(input, 100) == 67384529
}

static void testPart2() {
    ArrayList<Integer> input = "389125467".split("").collect{Integer.parseInt(it)}
    assert solvePart2(input, 10000000, 1000000) == 149245887792
}

class Cups {
    Cup head = null
    Cup tail = null
    Cup current = null
    int size = 0
    HashMap<Integer, Cup> cupsMap = new HashMap()

    public add(int label) {
        Cup cup = new Cup()
        cup.setLabel(label)
        cupsMap.put(label, cup)

        if(head == null) {
            this.head = cup
            this.tail = cup
            this.current = cup
            cup.setNext(cup)
        } else {
            this.head.setNext(cup)
            this.head = cup
            cup.setNext(this.tail)
        }
        size++
    }

    public Cup findCupWithLabel(int label) {
        return this.cupsMap.get(label)
    }

    public performMove() {

        // Cut out three cups
        Cup firstCup = current.next
        Cup secondCup = firstCup.next
        Cup thirdCup = secondCup.next
        current.setNext(thirdCup.next)

        // Find destination
        int destinationLabel = current.getLabel() - 1
        if(destinationLabel == 0) destinationLabel = size

        while(
                destinationLabel == firstCup.getLabel() ||
                destinationLabel == secondCup.getLabel() ||
                destinationLabel == thirdCup.getLabel()
        ) {
            destinationLabel--
            if(destinationLabel == 0) destinationLabel = size
        }

        // Paste three cups in after destination cup
        Cup destination = findCupWithLabel(destinationLabel)
        Cup destinationNext = destination.next

        // Link destination to next cup
        destination.setNext(firstCup)

        // Link third cup to cup after destination
        thirdCup.setNext(destinationNext)

        this.current = current.next
    }

    class Cup{
        int label
        Cup next;
    }

    public display() {
        Cup currentCup = this.tail
        String display = currentCup.getLabel()
        currentCup = currentCup.next

        while(currentCup != this.tail) {
            display += "  " + currentCup.getLabel()
            currentCup = currentCup.next
        }
        return display
    }

    public Long displayPart1() {
        Cup oneCup = findCupWithLabel(1)
        Cup currentCup = oneCup
        String display = ""
        currentCup = currentCup.next

        while(currentCup != oneCup) {
            display += currentCup.getLabel()
            currentCup = currentCup.next
        }
        return Long.parseLong(display)
    }

    public Long displayPart2() {
        Cup oneCup = findCupWithLabel(1)
        Long label1 = oneCup.next.getLabel()
        Long label2 = oneCup.next.next.getLabel()
        return label1 * label2
    }
}
