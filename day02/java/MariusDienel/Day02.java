import java.util.List;
import java.util.stream.Stream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

class Day02 {
    public static void main(String[] args) throws IOException{
        
        partOne();
        partTwo();
    }

    private static void partOne() throws IOException {
        long correctPasswordCount = Files.lines(Paths.get("day02.txt")).filter(line -> {
            String policy = line.split(":")[0];
            int minVal = Integer.valueOf(policy.split("-")[0]);
            int maxVal = Integer.valueOf(policy.split("-")[1].split(" ")[0]);
            String letterToContain = policy.substring(policy.length() - 1);

            String password = line.split(":")[1].substring(1);
            
            int count = 0;
            for(int i=0; i < password.length(); i++) {
                if (password.charAt(i) == letterToContain.charAt(0)) {
                    count++;
                }
            }

            if(minVal <= count && count <= maxVal) {
                return true;
            }
            return false;
         }).count();

        System.out.printf("Valid passwords '%s'", correctPasswordCount);
    }

    private static void partTwo() throws IOException {
        
       
         long correctPasswordCount = Files.lines(Paths.get("day02.txt")).filter(line -> {
            String policy = line.split(":")[0];
            int minVal = Integer.valueOf(policy.split("-")[0]);
            int maxVal = Integer.valueOf(policy.split("-")[1].split(" ")[0]);
            String letterToContain = policy.substring(policy.length() - 1);
            String password = line.split(":")[1].substring(1);
    
            boolean firstPositionContains = password.charAt(minVal - 1) == letterToContain.charAt(0);
            boolean secondPositionContains = password.charAt(maxVal - 1) == letterToContain.charAt(0);
            
            if(firstPositionContains && secondPositionContains) {
                return false;
            } 
            if(firstPositionContains || secondPositionContains) {
                return true;
            }

            return false;
         }).count();

        System.out.printf("Valid passwords part two '%s'", correctPasswordCount);
    }
}