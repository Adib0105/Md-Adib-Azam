import java.util.List;
/** Task Board - standalone Java portfolio application. */
class Project19 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(19, "Alpha", 39.0), new Item(20, "Beta", 49.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Task Board");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
