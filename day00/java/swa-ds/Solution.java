import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Solution {

    public static void main(String[] args) throws Exception {
        String greeting = Files.readString(Paths.get("input.txt"), StandardCharsets.UTF_8);
        System.out.printf("Hello %s!", greeting);
    }

}
