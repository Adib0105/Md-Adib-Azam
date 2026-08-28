import java.util.List;
/** Password Policy Validator - standalone Java portfolio application. */
class Project13 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(13, "Alpha", 33.0), new Item(14, "Beta", 43.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Password Policy Validator");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
