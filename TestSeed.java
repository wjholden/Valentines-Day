import java.util.Random;

public class TestSeed {
    public static void main (String args[]) {
        Random random = new Random(Long.valueOf(args[0]));
        for (int i = 0 ; i < Integer.valueOf(args[1]) ; i++) {
            System.out.println((char)(random.nextInt() & 0x7f | 0x20));
        }
    }
}