import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Expense Manager
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Expense(String category,double amount){}
    public static void main(String[]args){var grouped=List.of(new Expense("food",1200),new Expense("travel",700),new Expense("food",900),new Expense("learning",1500)).stream().collect(Collectors.groupingBy(Expense::category,TreeMap::new,Collectors.summingDouble(Expense::amount)));double income=30000,total=grouped.values().stream().mapToDouble(Double::doubleValue).sum();System.out.println(grouped);System.out.printf("spent=%.2f savings_rate=%.1f%%%n",total,(income-total)/income*100);}
}
