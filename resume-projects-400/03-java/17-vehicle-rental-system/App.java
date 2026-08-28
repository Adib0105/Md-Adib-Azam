import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Vehicle Rental System
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Rental(String vehicle,LocalDate start,LocalDate due,LocalDate returned,double dailyRate){}
    public static void main(String[]args){for(var r:List.of(new Rental("Bike",LocalDate.parse("2026-08-20"),LocalDate.parse("2026-08-23"),LocalDate.parse("2026-08-25"),500),new Rental("Car",LocalDate.parse("2026-08-21"),LocalDate.parse("2026-08-24"),LocalDate.parse("2026-08-24"),1800))){long days=Math.max(1,ChronoUnit.DAYS.between(r.start(),r.returned())),late=Math.max(0,ChronoUnit.DAYS.between(r.due(),r.returned()));double total=days*r.dailyRate()+late*r.dailyRate()*.5;System.out.printf("%s days=%d late=%d total=%.2f%n",r.vehicle(),days,late,total);}}
}
