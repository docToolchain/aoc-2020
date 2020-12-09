package cpu

class Parser {

    static void parse(String opcodes) {
        Vm.program = []
        Vm.state = [pointer:0, acc:0]
        opcodes.eachLine { line ->
            line = line.split(" ")
            Vm.program << [op:line[0],p1:[line[1] as Integer]]
        }
    }
}