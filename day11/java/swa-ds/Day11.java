import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.stream.Stream;

public class Day11 {

//tag::constants[]
    public static final char EMPTY = 'L';
    public static final char OCCUPIED = '#';
//end::constants[]

    public static void main(String[] args) throws IOException {

//tag::part1[]
        String input = String.join("\n", Files.readAllLines(Path.of("day11.txt")));

        Day11 solver = new Day11();

        int result = solver.solvePart1(input);
        System.out.println(result);
//end::part1[]


        result = solver.solvePart2(input);
        System.out.println(result);
    }

//tag::solvePart1[]
    public int solvePart1(String input) {
        char[][] waitingArea = fromString(input);
        boolean notEqual = true;

        while(notEqual) {
            char[][] waitingAreaNew = copy(waitingArea);

            for (int row = 0; row < waitingArea.length; row++) {
                for (int col = 0; col < waitingArea[row].length; col++) {
                    int occupied = countOccupiedAdjacent(waitingArea, row, col);
                    if (waitingArea[row][col] == EMPTY && occupied == 0) {
                        waitingAreaNew[row][col] = OCCUPIED;
                    } else if (waitingArea[row][col] == OCCUPIED && occupied >= 4) {
                        waitingAreaNew[row][col] = EMPTY;
                    }
                }
            }
            notEqual = !equal(waitingArea, waitingAreaNew);

            waitingArea = copy(waitingAreaNew);
        }

        return countAllOccupied(waitingArea);
    }

    int countOccupiedAdjacent(char[][] seatArea, int row, int col) {
        int count = 0;
        if (row > 0) {
            count = occupiedInRow(col, count, seatArea[row - 1]);
        }
        if (row < seatArea.length - 1) {
            count = occupiedInRow(col, count, seatArea[row + 1]);
        }
        if (col > 0 && seatArea[row][col - 1] == OCCUPIED) {
            count++;
        }
        if (col < seatArea[row].length - 1 && seatArea[row][col+1] == OCCUPIED) {
            count++;
        }
        return count;
    }

    private int occupiedInRow(int col, int count, char[] row) {
        if (col > 0 && row[col - 1] == OCCUPIED) {
            count++;
        }
        if (row[col] == OCCUPIED) {
            count++;
        }
        if (col < (row.length - 1) && row[col + 1] == OCCUPIED) {
            count++;
        }

        return count;
    }

//end::solvePart1[]

//tag::solvePart2[]
    public int solvePart2(String input) {
        char[][] waitingArea = fromString(input);
        boolean notEqual = true;

        while(notEqual) {
            char[][] waitingAreaNew;
            waitingAreaNew = copy(waitingArea);

            for (int row = 0; row < waitingArea.length; row++) {
                for (int col = 0; col < waitingArea[row].length; col++) {
                    int occupied = countVisibleOccupied(waitingArea, row, col);
                    if (waitingArea[row][col] == EMPTY && occupied == 0) {
                        waitingAreaNew[row][col] = OCCUPIED;
                    } else if (waitingArea[row][col] == OCCUPIED && occupied >= 5) {
                        waitingAreaNew[row][col] = EMPTY;
                    }
                }
            }
            notEqual = !equal(waitingArea, waitingAreaNew);

            waitingArea = copy(waitingAreaNew);
        }

        return countAllOccupied(waitingArea);
    }

    public int countVisibleOccupied(char[][] waitingArea, int row, int col) {
        int count = 0;
        // north
        if (nextVisibleSeatIsOccupied(waitingArea, row, col, -1, 0)) count++;
        // south
        if (nextVisibleSeatIsOccupied(waitingArea, row, col, 1, 0)) count++;
        // east
        if (nextVisibleSeatIsOccupied(waitingArea, row, col, 0, 1)) count++;
        // west
        if (nextVisibleSeatIsOccupied(waitingArea, row, col, 0, -1)) count++;
        // northeast
        if (nextVisibleSeatIsOccupied(waitingArea, row, col, -1, -1)) count++;
        // northwest
        if (nextVisibleSeatIsOccupied(waitingArea, row, col, -1, 1)) count++;
        // southeast
        if (nextVisibleSeatIsOccupied(waitingArea, row, col, 1, -1)) count++;
        // southwest
        if (nextVisibleSeatIsOccupied(waitingArea, row, col, 1, 1)) count++;

        return count;
    }

    private boolean nextVisibleSeatIsOccupied(char[][] waitingArea, int row, int col, int rowStep, int colStep) {
        int curRow = row + rowStep;
        int curCol = col + colStep;
        while (notOutOfBounds(curRow, curCol, waitingArea.length, waitingArea[0].length)) {
            if (waitingArea[curRow][curCol] == OCCUPIED) return true;
            if (waitingArea[curRow][curCol] == EMPTY) return false;
            curRow += rowStep;
            curCol += colStep;
        }
        return false;
    }

    private boolean notOutOfBounds(int curRow, int curCol, int rows, int cols) {
        return curRow >= 0 && curRow < rows && curCol >= 0 && curCol < cols;
    }
//end::solvePart2[]

//tag::common[]
    private int countAllOccupied(char[][] seatArea) {
        int count = 0;
        for (char[] seats : seatArea) {
            for (char seat : seats) {
                if (seat == OCCUPIED) {
                    count++;
                }
            }
        }
        return count;
    }

    private boolean equal(char[][] a, char[][] b) {
        for (int i = 0; i < a.length; i++) {
            if (!Arrays.equals(a[i], b[i])) {
                return false;
            }
        }
        return true;
    }

    char[][] copy(char[][] waitingArea) {
        char[][] copy = new char[waitingArea.length][];
        for (int i = 0; i < waitingArea.length; i++) {
            copy[i] = Arrays.copyOf(waitingArea[i], waitingArea[i].length);
        }
        return copy;
    }

    char[][] fromString(String str) {
        return Stream.of(str.split("\n"))
                .map(String::toCharArray)
                .toArray(char[][]::new);
    }
//end::common[]

}
