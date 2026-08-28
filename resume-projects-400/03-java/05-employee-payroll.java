import java.util.List;
/** Employee Payroll - standalone Java portfolio application. */
class Project05 {
    record Item(int id, String name, double value) {}
    public static void main(String[] args) {
        var items = List.of(new Item(5, "Alpha", 25.0), new Item(6, "Beta", 35.0));
        double total = items.stream().mapToDouble(Item::value).sum();
        System.out.println("Employee Payroll");
        items.forEach(System.out::println);
        System.out.printf("Total: %.2f | Average: %.2f%n", total, total / items.size());
    }
}
