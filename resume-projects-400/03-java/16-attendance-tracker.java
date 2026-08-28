import java.util.List;
/** Attendance Tracker - standalone Java portfolio application. */
class Project16 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(16, "Alpha", 36.0), new Item(17, "Beta", 46.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Attendance Tracker");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
