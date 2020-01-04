import java.util.*;

public class RandomMessage {

    private static long[] l = new long[] {
        247057036367419L, 35543432715160L, 253980514236592L, 89613466789088L,
        53058416132968L, 111106152524424L, 231264589651259L, 218141079436269L,
        203524665566275L, 99273655041031L, 217249958230482L
    };

    public static void main(String args[]) {
        for (int i = 0 ; i < l.length ; i++) {
            Random random = new Random(l[i]);
            System.out.print((char)(random.nextInt() & 95));
            System.out.print((char)(random.nextInt() & 95));
            System.out.print((char)(random.nextInt() & 95));
        }
    }
}
