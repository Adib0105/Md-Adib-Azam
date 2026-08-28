import java.util.List;
/** Restaurant Order Manager - standalone Java portfolio application. */
class Project18 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(18, "Alpha", 38.0), new Item(19, "Beta", 48.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Restaurant Order Manager");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
