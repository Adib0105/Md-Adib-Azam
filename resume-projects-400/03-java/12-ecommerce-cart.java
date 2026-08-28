import java.util.List;
/** Ecommerce Cart - standalone Java portfolio application. */
class Project12 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(12, "Alpha", 32.0), new Item(13, "Beta", 42.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Ecommerce Cart");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
