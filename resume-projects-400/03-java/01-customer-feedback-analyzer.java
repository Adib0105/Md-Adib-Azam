import java.util.List;
/** Customer Feedback Analyzer - standalone Java portfolio application. */
class Project01 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(1, "Alpha", 21.0), new Item(2, "Beta", 31.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Customer Feedback Analyzer");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
