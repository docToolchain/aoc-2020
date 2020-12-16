import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Day14 {

    private static final String ZERO_PADDING = "000000000000000000000000000000000000";

    public static void main(String[] args) throws IOException {
        List<String> program = Files.readAllLines(Path.of("day14.txt"));
        Day14 solver = new Day14();

        Map<Integer, Long> memory = new HashMap<>();
        char[] mask = null;

        for (String line : program) {
            if (line.startsWith("mask")) {
                mask = parseMask(line);
            } else {
                int address = Integer.parseInt(line.substring(line.indexOf('[')+1, line.indexOf(']')));
                int value = Integer.parseInt(line.substring(line.lastIndexOf(' ')+1));
                memory.put(address, solver.convert(value, mask));
            }
        }
        long result = memory.values().stream().mapToLong(l -> l.longValue()).sum();
        System.out.println(result);
    }

    private static char[] parseMask(String line) {
        return line.substring(line.length() - 36).toCharArray();
    }

    public String toBinaryString(long l) {
        return toBinarySb(l).toString();
    }

    public StringBuilder toBinarySb(long l) {
        StringBuilder sb = new StringBuilder(36);
        String bin = Long.toBinaryString(l);
        sb.append(ZERO_PADDING, 0, 36-bin.length());
        sb.append(bin);
        return sb;
    }

    long convert(long l, char[] mask) {
        StringBuilder binSb = toBinarySb(l);
        for (int i = 0; i < binSb.length(); i++) {
            if (mask[i] != 'X') {
                binSb.replace(i, i+1, Character.toString(mask[i]));
            }
        }
        return Long.parseLong(binSb.toString(), 2);
    }

}
