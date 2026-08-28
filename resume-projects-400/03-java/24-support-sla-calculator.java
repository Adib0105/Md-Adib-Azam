import java.util.List;
/** Support SLA Calculator - standalone Java portfolio application. */
class Project24 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(24, "Alpha", 44.0), new Item(25, "Beta", 54.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Support SLA Calculator");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
