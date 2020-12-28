import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static java.util.stream.Collectors.toList;

public class Day14 {

    private static final String ZERO_PADDING = "000000000000000000000000000000000000";

    public static void main(String[] args) throws IOException {
        List<String> program = Files.readAllLines(Path.of("day14.txt"));
        Day14 solver = new Day14();

        Map<Integer, Long> memory = new HashMap<>();

        long result = solver.part1(program, memory);
        System.out.println(result);

        // Part 2
        result = solver.part2(program);
        System.out.println(result);
    }

    private long part1(List<String> program, Map<Integer, Long> memory) {
        // Part 1
        char[] mask = null;
        for (String line : program) {
            if (line.startsWith("mask")) {
                mask = parseMask(line);
            } else {
                int address = Integer.parseInt(line.substring(line.indexOf('[')+1, line.indexOf(']')));
                int value = Integer.parseInt(line.substring(line.lastIndexOf(' ')+1));
                memory.put(address, convert(value, mask));
            }
        }
        return memory.values().stream().mapToLong(Long::longValue).sum();
    }

    private static char[] parseMask(String line) {
        return line.substring(line.length() - 36).toCharArray();
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

    long part2(List<String> program) {
        Map<Long, Long> memory = new HashMap<>();
        String mask = null;
        long result;
        for (String line : program) {
            if (line.startsWith("mask")) {
                mask = line.substring(line.length() - 36);
            } else {
                long value = Long.parseLong(line.substring(line.lastIndexOf(' ')+1));
                int address = Integer.parseInt(line.substring(line.indexOf('[')+1, line.indexOf(']')));

                String addressMask = getAddressMask(address, mask);
                List<Long> addresses = getAddresses(address, addressMask);
                for (Long addr : addresses) {
                    memory.put(addr, value);
                }
            }
        }
        result = memory.values().stream().mapToLong(Long::longValue).sum();
        return result;
    }

    private String getAddressMask(int address, String mask) {
        String addressBin = toBinaryString(address);
        StringBuilder addressMask = new StringBuilder(36);
        for (int i = 0; i < addressBin.length(); i++) {
            if (mask.charAt(i) == '0') {
                addressMask.append(addressBin.charAt(i));
            } else if (mask.charAt(i) == '1') {
                addressMask.append('1');
            } else if (mask.charAt(i) == 'X') {
                addressMask.append('X');
            }
        }
        return addressMask.toString();
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

    List<Long> getAddresses(long address, String mask) {
        List<String> masks = getMemoryMasks(mask);
        return masks.stream()
                .map(String::toCharArray)
                .map(m -> convert(address, m))
                .collect(toList());
    }

    List<String> getMemoryMasks(String mask) {
        ArrayList<String> masks = new ArrayList<>();
        masks.add(mask);
        boolean hasFloating = true;
        while (hasFloating) {
            hasFloating = false;
            for (int i = 0; i < masks.size(); i++) {
                String m = masks.get(i);
                int floatingIdx = m.indexOf('X');
                if (floatingIdx >= 0) {
                    hasFloating = true;
                    masks.remove(m);
                    masks.add(m.substring(0, floatingIdx) + '0' + m.substring(floatingIdx + 1));
                    masks.add(m.substring(0, floatingIdx) + '1' + m.substring(floatingIdx + 1));
                }
            }
        }

        return masks;
    }

}
