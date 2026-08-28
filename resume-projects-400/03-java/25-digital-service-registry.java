import java.util.List;
/** Digital Service Registry - standalone Java portfolio application. */
class Project25 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(25, "Alpha", 45.0), new Item(26, "Beta", 55.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Digital Service Registry");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
