import java.util.List;
/** Hotel Booking Console - standalone Java portfolio application. */
class Project07 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(7, "Alpha", 27.0), new Item(8, "Beta", 37.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Hotel Booking Console");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
