import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Supplier;

public class Day08 {

    public static void main(String[] args) throws IOException {
//tag::mainPart1[]
        List<String> linesOfCode = Files.readAllLines(Path.of("day08.txt"));

        // Part 1
        Program program = Parser.parse(linesOfCode);
        program.run();
        System.out.println(program.getState().accumulator);
//end::mainPart1[]

//tag::mainPart2[]
        for (int idx = 0; idx < linesOfCode.size(); idx++) {
            program = Parser.parse(linesOfCode);  // <1>
            Operation op = program.operations[idx]; // <2>
            if (op instanceof Jmp) {
                program.replaceOperationWith(idx,
                        Operation.newOperation(op.value, Nop::new)); // <3>
            } else if (op instanceof Nop) {
                program.replaceOperationWith(idx,
                        Operation.newOperation(op.value, Jmp::new)); // <4>
            }
            var exitCode = program.run();
            if (exitCode == ExitCode.NORMAL) { // <5>
                System.out.println(program.getState().accumulator);
                break;
            }
        }
//end::mainPart2[]
    }
}


//tag::program[]
enum ExitCode { NORMAL, INFINITE_LOOP }

class Program {

    static class State {
        int opPointer;
        int accumulator;
    }

    private final boolean debug = false;

    public void replaceOperationWith(int i, Operation newOperation) {
        operations[i] = newOperation;
    }

    Operation[] operations;

    State state = new State();

    ExitCode run() {
        int count = 0;
        while (true) {
            if (state.opPointer == operations.length) {
                return ExitCode.NORMAL; // <1>
            }
            Operation operation = operations[state.opPointer];
            if (debug) System.out.print(count + ". Executing " + operation);
            if (operation.alreadyExecuted) {
                return ExitCode.INFINITE_LOOP; // <2>
            } else {
                operation.execute(state);
                operation.alreadyExecuted = true; // <3>
                state.opPointer++;
            }
            if (debug) System.out.println(" - accum: " + state.accumulator);
        }
    }

    State getState() {
        return state;
    }

}
//end::program[]

//tag::ops[]
abstract class Operation {
    int     value;
    boolean alreadyExecuted = false;

    abstract void execute(Program.State state);

    public String toString() {
        return getClass().getSimpleName() + " " + (value >= 0 ? "+" : "") + value;
    }

    static Operation newOperation(int value, Supplier<Operation> opSupplier) { // <1>
        Operation newOp = opSupplier.get();
        newOp.value = value;
        return newOp;
    }
}

class Nop extends Operation {
    @Override
    void execute(Program.State state) {
        // nothing to do
    }
}
class Acc extends Operation {
    @Override
    void execute(Program.State state) {
        state.accumulator += value;
    }
}
class Jmp extends Operation {
    @Override
    void execute(Program.State state) {
        state.opPointer += value;
        state.opPointer--; // will be increased again by the program after the jmp is executed, so we'll have to decrease it here
    }
}
//end::ops[]


//tag::parser[]
class Parser {

    private static final Map<String, Supplier<Operation>> OPERATIONS = new HashMap<>();

    static {
        OPERATIONS.put("nop", Nop::new);
        OPERATIONS.put("acc", Acc::new);
        OPERATIONS.put("jmp", Jmp::new);
    }

    static Operation toOperation(String lineOfCode) {
        String[] split = lineOfCode.split(" ");
        Supplier<Operation> opSupplier = OPERATIONS.get(split[0]);
        if (opSupplier == null) {
            throw new IllegalArgumentException("Instruction '" + split[0] + "' is not supported");
        }
        Operation op = opSupplier.get(); // <1>
        op.value = Integer.parseInt(split[1]); // <2>
        return op;
    }

    public static Program parse(List<String> linesOfCode) {
        Program newProgram = new Program();
        newProgram.operations = linesOfCode.stream()
                .map(Parser::toOperation)
                .toArray(Operation[]::new);
        return newProgram;
    }
}
//end::parser[]
