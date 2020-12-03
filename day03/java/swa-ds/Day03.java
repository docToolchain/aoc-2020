import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class Day03 {

//tag::createMap[]
    public int countTrees(List<String> lines, int stepsRight, int stepsDown) {
        char[][] map = lines.stream()
                .map(String::toCharArray)
                .toArray(char[][]::new);
//end::createMap[]

//tag::solution[]
/*              right
        + - - - - >
        |
        |
        |
        v
      down
*/
        int right = 0;
        int down = 0;
        int mapWidth = map[0].length;

        int treeCount = 0;
        while (down < map.length) {
            if (map[down][right] == '#') {
                treeCount++;
            }
            right = (right + stepsRight) % mapWidth; // <1>
            down += stepsDown;
        }
        return treeCount;
    }
//end::solution[]

    public static void main(String[] args) throws IOException {
//tag::part1Output[]
        List<String> lines = Files.readAllLines(Paths.get("day03.txt"));

        Day03 solver = new Day03();

        // Part I
        int treeCount = solver.countTrees(lines, 3, 1); // <1>

        System.out.println("Part I: " + treeCount);
//end::part1Output[]

//tag::part2Output[]
        long solution = solver.countTrees(lines, 1, 1);
        solution *= solver.countTrees(lines, 3, 1);
        solution *= solver.countTrees(lines, 5, 1);
        solution *= solver.countTrees(lines, 7, 1);
        solution *= solver.countTrees(lines, 1, 2);

        System.out.println("Part II: " + solution);
//end::part2Output[]
    }

}


