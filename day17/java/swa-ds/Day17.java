import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class Day17 {

    public static void main(String[] args) throws IOException {
//tag::mainPart1[]
        List<String> input = Files.readAllLines(Path.of("day17.txt"));

        PocketDimension3D dim3D = new PocketDimension3D();
        dim3D.init(21, input);

        for (int i = 0; i < 6; i++) {
            dim3D.transition();
        }

        int result = dim3D.countActiveCubes();
        System.out.println("Solution of Part I  >>> " + result);
//end::mainPart1[]

//tag::mainPart2[]
        PocketDimension4D dim4D = new PocketDimension4D();
        dim4D.init(21, input);

        for (int i = 0; i < 6; i++) {
            dim4D.transition();
        }

        result = dim4D.countActiveCubes();
        System.out.println("Solution of Part II >>> " + result);
    }
//end::mainPart2[]
}

//tag::part1[]
class PocketDimension3D {

    private static final char INACTIVE = '.';
    private static final char ACTIVE = '#';

    private char[][][] cubes;

    private int a;
    private int offset;

    public void init(int a, List<String> initialState) {
        this.a = a;
        int height = initialState.size();
        offset = (a - height - 1) / 2;
        cubes = new char[a][a][a];
        for (int x = 0; x < a; x++) {
            for (int y = 0; y < a; y++) {
                for (int z = 0; z < a; z++) {
                    cubes[x][y][z] = INACTIVE;
                }
            }
        }
        fill(initialState);
    }

    private void fill(List<String> initialStates) {
        char[][] chars = initialStates.stream().map(String::toCharArray).toArray(char[][]::new);
        int z = 0;
        for (int x = 0; x < chars.length; x++) {
            for (int y = 0; y < chars[x].length; y++) {
                setWithOffset(x, y, z, chars[x][y]);
            }
        }
    }

    private void setWithOffset(int x, int y, int z, char state) {
        cubes[x + offset][y + offset][z + offset] = state;
    }

    public void transition() {
        ArrayList<Transition3D> transitions = new ArrayList<>();  // <1>
        for (int x = 0; x < a; x++) {
            for (int y = 0; y < a; y++) {
                for (int z = 0; z < a; z++) {
                    int activeNeighbours = countActiveNeighbours(x, y, z);
                    if (cubes[x][y][z] == ACTIVE && activeNeighbours != 2 && activeNeighbours != 3) {
                        transitions.add(new Transition3D(x, y, z, INACTIVE)); // <1>
                    } else if (cubes[x][y][z] == INACTIVE && activeNeighbours == 3) {
                        transitions.add(new Transition3D(x, y, z, ACTIVE));  // <1>
                    }
                }
            }
        }
        transitions.forEach(t -> cubes[t.x][t.y][t.z] = t.newState); // <2>
    }

    private int countActiveNeighbours(int x, int y, int z) { // <3>
        int count = 0;
        for (int dX = -1; dX <= 1; dX++) {
            for (int dY = -1; dY <= 1; dY++) {
                for (int dZ = -1; dZ <= 1; dZ++) {
                    if (dX == 0 && dY == 0 && dZ == 0) continue;
                    if (isActive(x + dX, y + dY, z + dZ)) count++;
                }
            }
        }
        return count;
    }

    private boolean isActive(int x, int y, int z) {
        if (outOfBounds(x) || outOfBounds(y) || outOfBounds(z)) {
            return false;
        }
        return cubes[x][y][z] == ACTIVE;
    }

    private boolean outOfBounds(int i) {
        return i < 1 || i > a - 1;
    }

    public int countActiveCubes() {
        int count = 0;
        for (char[][] cube : cubes) {
            for (char[] square : cube) {
                for (char state : square) {
                    if (state == ACTIVE) count++;
                }
            }
        }
        return count;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int z = 0; z < a; z++) {
            StringBuilder sbsquare = new StringBuilder("z=" + (z - offset) + "\n");
            boolean hasActive = false;
            for (int y = 0; y < a; y++) {
                for (int x = 0; x < a; x++) {
                    char state = cubes[y][x][z];
                    sbsquare.append(state);
                    if (state == ACTIVE) {
                        hasActive = true;
                    }
                }
                sbsquare.append("\n");
            }
            if (hasActive) {
                sbsquare.append("===\n");
                sb.append(sbsquare);
            }
        }
        return sb.toString();
    }
}

class Transition3D {

    int x, y, z;
    char newState;

    Transition3D(int x, int y, int z, char newState) {
        this.x = x;
        this.y = y;
        this.z = z;
        this.newState = newState;
    }
}
//end::part1[]

//tag::part2[]
class PocketDimension4D {

    private static final char INACTIVE = '.';
    private static final char ACTIVE = '#';

    private char[][][][] cubes;

    private int a;
    private int offset;

    public void init(int a, List<String> initialState) {
        this.a = a;
        int height = initialState.size();
        offset = (a - height - 1) / 2;
        cubes = new char[a][a][a][a];
        for (int x = 0; x < a; x++) {
            for (int y = 0; y < a; y++) {
                for (int z = 0; z < a; z++) {
                    for (int w = 0; w < a; w++) {
                        cubes[x][y][z][w] = INACTIVE;
                    }
                }
            }
        }
        fill(initialState);
    }

    private void fill(List<String> initialStates) {
        char[][] chars = initialStates.stream().map(String::toCharArray).toArray(char[][]::new);
        int z = 0;
        int w = 0;
        for (int x = 0; x < chars.length; x++) {
            for (int y = 0; y < chars[x].length; y++) {
                setWithOffset(x, y, z, w, chars[x][y]);
            }
        }
    }

    private void setWithOffset(int x, int y, int z, int w, char state) {
        cubes[x + offset][y + offset][z + offset][w + offset] = state;
    }

    public void transition() {
        ArrayList<Transition4D> transitions = new ArrayList<>();
        for (int x = 0; x < a; x++) {
            for (int y = 0; y < a; y++) {
                for (int z = 0; z < a; z++) {
                    for (int w = 0; w < a; w++) {
                        int activeNeighbours = countActiveNeighbours(x, y, z, w);
                        if (cubes[x][y][z][w] == ACTIVE && activeNeighbours != 2 && activeNeighbours != 3) {
                            transitions.add(new Transition4D(x, y, z, w, INACTIVE));
                        } else if (cubes[x][y][z][w] == INACTIVE && activeNeighbours == 3) {
                            transitions.add(new Transition4D(x, y, z, w, ACTIVE));
                        }
                    }
                }
            }
        }
        transitions.forEach(t -> cubes[t.x][t.y][t.z][t.w] = t.newState);
    }

    private int countActiveNeighbours(int x, int y, int z, int w) {
        int count = 0;
        for (int dX = -1; dX <= 1; dX++) {
            for (int dY = -1; dY <= 1; dY++) {
                for (int dZ = -1; dZ <= 1; dZ++) {
                    for (int dW = -1; dW <= 1; dW++) {
                        if (dX == 0 && dY == 0 && dZ == 0 && dW == 0) continue;
                        if (isActive(x + dX, y + dY, z + dZ, w + dW)) count++;
                    }
                }
            }
        }
        return count;
    }

    private boolean isActive(int x, int y, int z, int w) {
        if (outOfBounds(x) || outOfBounds(y) || outOfBounds(z) || outOfBounds(w)) {
            return false;
        }
        return cubes[x][y][z][w] == ACTIVE;
    }

    private boolean outOfBounds(int i) {
        return i < 1 || i > a - 1;
    }

    public int countActiveCubes() {
        int count = 0;
        for (char[][][] cubes3d : cubes) {
            for (char[][] cube : cubes3d) {
                for (char[] square : cube) {
                    for (char state : square) {
                        if (state == ACTIVE) count++;
                    }
                }
            }
        }
        return count;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int w = 0; w < a; w++) {
            for (int z = 0; z < a; z++) {
                StringBuilder sbsquare = new StringBuilder("z=" + (z - offset) + " + w=" + (w - offset) + ":\n");
                boolean hasActive = false;
                for (int y = 0; y < a; y++) {
                    for (int x = 0; x < a; x++) {
                        char state = cubes[y][x][z][w];
                        sbsquare.append(state);
                        if (state == ACTIVE) {
                            hasActive = true;
                        }
                    }
                    sbsquare.append("\n");
                }
                if (hasActive) {
                    sb.append(sbsquare);
                }
            }
        }
        return sb.toString();
    }
}

class Transition4D extends Transition3D {

    int w;

    Transition4D(int x, int y, int z, int w, char newState) {
        super(x, y, z, newState);
        this.w = w;
    }
}
//end::part2[]
