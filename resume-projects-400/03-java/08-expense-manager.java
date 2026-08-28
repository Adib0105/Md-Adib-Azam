import java.util.List;
/** Expense Manager - standalone Java portfolio application. */
class Project08 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(8, "Alpha", 28.0), new Item(9, "Beta", 38.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Expense Manager");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
