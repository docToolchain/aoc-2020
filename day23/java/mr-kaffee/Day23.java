import java.util.Arrays;

public class Day23 {

    // tag::solve[]
    public static Item solve(int[] data0, int len, int rounds) {
        int[] data = new int[len];
        System.arraycopy(data0, 0, data, 0, data0.length);
        for (int k = data0.length; k < len; k++) {
            data[k] = k + 1;
        }

        Item[] items = Item.build(data);
        Item head = items[0];
        Item low = items[1];

        Item curr = head;
        for (int k = 0; k < rounds; k++) {
            Item n1 = curr.next;
            Item n2 = n1.next;
            Item n3 = n2.next;

            curr.next = n3.next;

            Item dest = curr.low;
            while (dest == n1 || dest == n2 || dest == n3) {
                dest = dest.low;
            }

            n3.next = dest.next;
            dest.next = n1;

            curr = curr.next;
        }

        return low;
    }
    // end::solve[]

    public static void main(String[] args) {
        int[] data0 = new int[]{4, 8, 7, 9, 1, 2, 3, 6, 5};

        {
            long t = System.currentTimeMillis();
            Item low = solve(data0, data0.length, 100);
            Item a = low.next;
            long sol = 0;
            do {
                sol = sol * 10 + a.value;
                a = a.next;
            } while (a != low);
            System.out.format("Part 1 solved in %d ms -> %d%n", System.currentTimeMillis() - t, sol);
            assert sol == 89_573_246;
        }

        {
            long t = System.currentTimeMillis();
            Item low = solve(data0, 1_000_000, 10_000_000);
            long n1 = low.next.value;
            long n2 = low.next.next.value;
            System.out.format("Part 2 solved in %d ms -> n1: %d, n2: %d, n1 * n2: %d%n",
                    System.currentTimeMillis() - t, n1, n2, n1 * n2);
            assert n1 * n2 == 2_029_056_128;
        }
    }

    // tag::item[]
    static final class Item implements Comparable<Item> {
        static Item[] build(int[] data) {
            Item[] items = new Item[data.length];
            items[0] = new Item(data[0]);

            for (int k = 1; k < data.length; k++) {
                items[k] = new Item(data[k]);
                items[k - 1].next = items[k];
            }
            items[items.length - 1].next = items[0];

            Item head = items[0];

            Arrays.sort(items);
            for (int k = 0; k < data.length; k++) {
                items[k].low = items[k == 0 ? data.length - 1 : k - 1];
            }

            Item low = items[0];

            return new Item[]{head, low};
        }


        Item next;
        Item low;
        int value;

        Item(int value) {
            this.value = value;
            this.next = this;
            this.low = this;
        }

        @Override
        public int compareTo(Item o) {
            return Integer.compare(this.value, o.value);
        }

        @Override
        public String toString() {
            return String.format("Item(%d)", value);
        }
    }
    // end::item[]
}
