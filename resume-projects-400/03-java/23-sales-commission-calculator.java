import java.util.List;
/** Sales Commission Calculator - standalone Java portfolio application. */
class Project23 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(23, "Alpha", 43.0), new Item(24, "Beta", 53.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Sales Commission Calculator");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
