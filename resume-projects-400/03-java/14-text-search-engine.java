import java.util.List;
/** Text Search Engine - standalone Java portfolio application. */
class Project14 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(14, "Alpha", 34.0), new Item(15, "Beta", 44.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Text Search Engine");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
