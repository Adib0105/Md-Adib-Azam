import java.util.List;
/** Banking Console - standalone Java portfolio application. */
class Project02 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(2, "Alpha", 22.0), new Item(3, "Beta", 32.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Banking Console");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
