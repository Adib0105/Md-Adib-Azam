import java.util.List;
/** URL Validator - standalone Java portfolio application. */
class Project22 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(22, "Alpha", 42.0), new Item(23, "Beta", 52.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("URL Validator");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
