import java.util.List;
/** Vehicle Rental System - standalone Java portfolio application. */
class Project17 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(17, "Alpha", 37.0), new Item(18, "Beta", 47.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Vehicle Rental System");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
