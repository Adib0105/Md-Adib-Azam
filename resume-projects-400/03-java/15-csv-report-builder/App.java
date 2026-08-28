import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * CSV Report Builder
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Sale(String month,String category,double amount){}
    public static void main(String[]args){var csv=List.of("month,category,amount","Jan,Design,1200","Jan,Hosting,800","Feb,Design,1500");var sales=csv.stream().skip(1).map(x->x.split(",")).map(x->new Sale(x[0],x[1],Double.parseDouble(x[2]))).toList();var totals=sales.stream().collect(Collectors.groupingBy(Sale::month,LinkedHashMap::new,Collectors.summingDouble(Sale::amount)));System.out.println("| Month | Revenue |");System.out.println("|---|---:|");totals.forEach((k,v)->System.out.printf("| %s | %.2f |%n",k,v));}
}
