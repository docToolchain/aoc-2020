import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Stream;

import static java.util.stream.Collectors.toList;

public class Day13 {
    public static void main(String[] args) throws IOException {
        List<String> input = Files.readAllLines(Path.of("day13.txt"));

        Day13 solver = new Day13();

        // Part 1
        System.out.println("Part 1: " + solver.nextBus(input));

        // Part 2
        long solutionPart2 = solver.seriesStartTimestamp(input.get(1));
        System.out.println("Part 2: " + solutionPart2);
    }

    public int nextBus(List<String> input) {
        int earliestDeparture = Integer.parseInt(input.get(0));

        List<Integer> buses = Stream.of(input.get(1).split(","))
                .filter(id -> !"x".equals(id))
                .map(Integer::valueOf)
                .collect(toList());

        for (int time = 1; time < 1_000_000; time++) {
            for (Integer id : buses) {
                int departure = id * time;
                if (departure > earliestDeparture) {
                    int waitingTime = departure - earliestDeparture;
                    System.out.println("time=" + time + " id=" + id + " wait=" + waitingTime);
                    return waitingTime * id;
                }
            }
        }

        return -1;
    }

    public long seriesStartTimestamp(String input) {
        List<String> split = Arrays.stream(input.split(","))
                .collect(toList());

        List<Bus> buses = new ArrayList<>(split.size());
        for (int offset = 0; offset < split.size(); offset++) {
            String s = split.get(offset);
            if (!"x".equals(s)) {
                Bus bus = new Bus(Integer.parseInt(s), offset);
                buses.add(bus);
            }
        }

        // solution thanks to James Hockenberry!
        long refTime = buses.get(0).id;
        long timeFixed = 0;
        for (Bus bus : buses) {
            long i = 0;
            while ((timeFixed + refTime * i + bus.offset) % bus.id != 0) {
                i += 1;
            }
            timeFixed = timeFixed + refTime * i;
            if (bus.offset != 0) {
                refTime = refTime * bus.id;
            }
        }
        return timeFixed;
    }
}

class Bus {
    int id;
    int offset;

    Bus(int id, int offset) {
        this.id = id;
        this.offset = offset;
    }
}