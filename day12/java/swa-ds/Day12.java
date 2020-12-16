import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;

public class Day12 {

    public int calcDistancePart1(List<String> input) {
        Ship ship = new Ship();
        input.stream()
                .map(Move::new)
                .forEach(ship::movePart1);

        return Math.abs(ship.x) + Math.abs(ship.y);
    }

    public int calcDistancePart2(List<String> input) {
        Ship ship = new Ship();
        input.stream()
                .map(Move::new)
                .forEach(ship::movePart2);

        return Math.abs(ship.x) + Math.abs(ship.y);
    }

    public static void main(String[] args) throws IOException {
        List<String> input = Files.readAllLines(Path.of("day12.txt"));

        // Part 1
        int distance = new Day12().calcDistancePart1(input);
        System.out.println(distance);

        // Part 2
        distance = new Day12().calcDistancePart2(input);
        System.out.println(distance);
    }

}

enum Direction {

    NORTH, EAST, SOUTH, WEST;

    public static Direction of(char direction) {
        for (Direction dir : values()) {
            if (dir.name().charAt(0) == direction) {
                return dir;
            }
        }
        throw new IllegalArgumentException("No such direction '" + direction + "'");
    }

    Direction turn(int degrees) {
        Direction[] directions = values();
        int dirIdx = Arrays.binarySearch(directions, this);

        int turns = degrees / 90;
        dirIdx = (dirIdx + turns) % directions.length;
        if (dirIdx < 0) {
            dirIdx = directions.length + dirIdx;
        }

        return directions[dirIdx];
    }

}

class Move {

    final char direction;
    final int units;

    Move(String s) {
        direction = s.charAt(0);
        units = Integer.parseInt(s.substring(1));
    }
}

class Ship {

    Direction currentDir = Direction.EAST;

    // ship's position
    int x = 0;
    int y = 0;

    // waypoint
    int wpX = 10; // East
    int wpY = 1;  // North

    void movePart1(Move move) {
        if (move.direction == 'R') {
            currentDir = currentDir.turn(move.units);
        } else if (move.direction == 'L') {
            currentDir = currentDir.turn(-1 * move.units);
        } else {
            Direction dirToMove;
            if (move.direction == 'F') {
                dirToMove = currentDir;
            } else {
                dirToMove = Direction.of(move.direction);
            }
            if (dirToMove == Direction.NORTH) {
                y -= move.units;
            } else if (dirToMove == Direction.EAST) {
                x += move.units;
            } else if (dirToMove == Direction.SOUTH) {
                y += move.units;
            } else if (dirToMove == Direction.WEST) {
                x -= move.units;
            }
        }
    }

    void movePart2(Move move) {
        if (move.direction == 'R') {
            rotateWp(move.units, true);
        } else if (move.direction == 'L') {
            rotateWp(move.units, false);
        } else if (move.direction == 'F') {
            int deltaX = wpX - x;
            int deltaY = wpY - y;
            x += deltaX * move.units;
            y += deltaY * move.units;
            wpX += deltaX * move.units;
            wpY += deltaY * move.units;
        } else {
            Direction dir = Direction.of(move.direction);
            if (dir == Direction.NORTH) {
                wpY += move.units;
            } else if (dir == Direction.EAST) {
                wpX += move.units;
            } else if (dir == Direction.SOUTH) {
                wpY -= move.units;
            } else if (dir == Direction.WEST) {
                wpX -= move.units;
            }
        }
    }

    private void rotateWp(int degrees, boolean clockwise) {
        wpX = wpX - x;
        wpY = wpY - y;
        for (int i = 0; i < degrees / 90; i++) {
            if (clockwise) {
                int wpXOld = wpX;
                wpX = wpY;
                wpY = wpXOld * -1;
            } else {
                int wpXdOld = wpX;
                wpX = wpY * -1;
                wpY = wpXdOld;
            }
        }
        wpX = wpX + x;
        wpY = wpY + y;
    }
}

