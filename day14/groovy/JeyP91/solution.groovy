import java.lang.reflect.Array

test()
solve()

void solve() {
    // tag::splitInput[]
    ArrayList<String> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator")))
    // end::splitInput[]
    println("Solution Part 1: " + solvePart1(input))
    println("Solution Part 2: " + solvePart2(input))
}

Long solvePart1(ArrayList<String> input) {
    // tag::solvePart1[]
    ArrayList<Integer> values = new ArrayList()
    String currentMask = ""
    for(int i = 0; i < input.size(); i++) {
        if(input[i].startsWith("mask")) {
            currentMask = getMaskFromInput(input[i])
        }
        if(input[i].startsWith("mem")) {
            int address = getAddressFromInput(input[i])
            int value = getValueFromInput(input[i])
            values = writeValuePart1(values, currentMask, value, address)
        }
    }
    return values.sum()
    // end::solvePart1[]
}

Long solvePart2(ArrayList<String> input) {
    // tag::solvePart2[]
    HashMap<Long, Long> values = new HashMap()
    String currentMask = ""
    for(int i = 0; i < input.size(); i++) {
        if(input[i].startsWith("mask")) {
            currentMask = getMaskFromInput(input[i])
        }
        if(input[i].startsWith("mem")) {
            Long address = getAddressFromInput(input[i])
            address |= getORMask(currentMask)
            ArrayList addresses = getAllAddresses(address, currentMask)
            int value = getValueFromInput(input[i])
            addresses.forEach{Long singleAddress ->
                values.put(singleAddress, value)
            }
        }
    }
    Long sum = 0
    // values.values().sum() is giving a wrong value most likely because of Integer Overflowg
    values.values().forEach{
        sum += it
    }
    return sum
    // end::solvePart2[]
}

String getMaskFromInput(String input) {
    return input.split(" = ")[1]
}

int getAddressFromInput(String input) {
    return Integer.parseInt(input.split('\\[')[1].split('\\]')[0])
}

int getValueFromInput(String input) {
    return Integer.parseInt(input.split(" = ")[1])
}

Long getANDMask(String mask) {
    mask = mask.replace('X', '1')
    return Long.parseLong(mask, 2)
}

Long getORMask(String mask) {
    mask = mask.replace('X', '0')
    return Long.parseLong(mask, 2)
}

Long applyMaskPart1(Long value, String mask) {
    value = value & getANDMask(mask)
    value = value | getORMask(mask)
    return value
}

ArrayList<Long> writeValuePart1(ArrayList<Long> values, String currentMask, Long value, int address) {
    while(values.size < address + 1) {
        values.add(0)
    }
    values.set(address, applyMaskPart1(value, currentMask))
    return values
}

ArrayList<Long> getAllAddresses(Long address, String mask) {
    ArrayList<Long> addresses = new ArrayList()
    int index = mask.indexOf('X')
    Long maskZeroed = ~(1 as long << ((mask.length() - index - 1)) as long)
    Long addressZeroed = address & maskZeroed
    Long maskOned = 1 as long << (mask.length() - index - 1) as long
    Long addressOned = address | maskOned
    int xCount = mask.count('X')
    if(xCount == 1) {
        addresses.add(addressZeroed)
        addresses.add(addressOned)
    } else {
        addresses.addAll(getAllAddresses(addressZeroed, mask.replaceFirst("X", "0")))
        addresses.addAll(getAllAddresses(addressOned, mask.replaceFirst("X", "1")))
    }
    return addresses
}

void test() {
    ArrayList<String> input1 = Arrays.asList(new File('input_test_1.txt').text.split(System.getProperty("line.separator")))
    assert getMaskFromInput("mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X") == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"
    assert getAddressFromInput("mem[8] = 11") == 8
    assert getValueFromInput("mem[8] = 11") == 11
    assert getAddressFromInput("mem[7] = 101") == 7
    assert getValueFromInput("mem[7] = 101") == 101
    assert getAddressFromInput("mem[8] = 0") == 8
    assert getValueFromInput("mem[8] = 0") == 0
    assert getANDMask("1X1") == 7
    assert getORMask("1X1") == 5
    assert applyMaskPart1(11, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X") == 73
    assert applyMaskPart1(101, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X") == 101
    assert applyMaskPart1(0, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X") == 64
    assert solvePart1(input1) == 165

    ArrayList<String> input2 = Arrays.asList(new File('input_test_2.txt').text.split(System.getProperty("line.separator")))
    String mask = getMaskFromInput(input2[0])
    int address = getAddressFromInput(input2[1])
    address |= getORMask(mask)
    ArrayList<Integer> addresses = getAllAddresses(address, mask)
    assert addresses[0] == 26
    assert addresses[1] == 27
    assert addresses[2] == 58
    assert addresses[3] == 59
    assert solvePart2(input2) == 208
}