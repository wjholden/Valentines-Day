import java.util.*;

public class RandomMessage {

    static Map<Long,Integer> s;

    static {
        s = new LinkedHashMap<>();
        s.put(238344791200146L, 1);
        s.put(173881529074270L, 3);
        s.put(242751563301421L, 1);
        s.put(165072168521792L, 3);
        s.put(141706662123585L, 5);
        s.put(141063381304714L, 2);
        s.put(177401611350426L, 3);
        s.put(244895512287375L, 2);
        s.put(195989853273583L, 4);
        s.put(50779719227499L, 3);
        s.put(21667526779401L, 3);
        s.put(187591116637459L, 3);
    }

    public static void main(String args[]) {
        s.forEach((k,v) -> {
            Random random = new Random(k);
            for (int i = 0 ; i < v ; i++) {
                System.out.print((char)(random.nextInt() & 95));
            }
        });
    }
}
