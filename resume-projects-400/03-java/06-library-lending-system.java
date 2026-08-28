import java.util.List;
/** Library Lending System - standalone Java portfolio application. */
class Project06 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(6, "Alpha", 26.0), new Item(7, "Beta", 36.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Library Lending System");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
