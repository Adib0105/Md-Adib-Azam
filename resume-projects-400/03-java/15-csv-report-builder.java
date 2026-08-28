import java.util.List;
/** CSV Report Builder - standalone Java portfolio application. */
class Project15 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(15, "Alpha", 35.0), new Item(16, "Beta", 45.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("CSV Report Builder");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
