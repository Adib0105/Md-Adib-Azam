import java.util.List;
/** Chat Message Model - standalone Java portfolio application. */
class Project21 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(21, "Alpha", 41.0), new Item(22, "Beta", 51.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Chat Message Model");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
