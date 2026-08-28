import java.util.List;
/** Quiz Application - standalone Java portfolio application. */
class Project09 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(9, "Alpha", 29.0), new Item(10, "Beta", 39.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Quiz Application");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
