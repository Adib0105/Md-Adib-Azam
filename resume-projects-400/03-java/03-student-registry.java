import java.util.List;
/** Student Registry - standalone Java portfolio application. */
class Project03 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(3, "Alpha", 23.0), new Item(4, "Beta", 33.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Student Registry");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
