import java.util.List;
/** Contact Manager - standalone Java portfolio application. */
class Project10 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(10, "Alpha", 30.0), new Item(11, "Beta", 40.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Contact Manager");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
