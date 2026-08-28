import java.util.List;
/** Inventory Service - standalone Java portfolio application. */
class Project04 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(4, "Alpha", 24.0), new Item(5, "Beta", 34.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Inventory Service");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
