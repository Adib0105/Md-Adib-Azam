import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Hotel Booking Console
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Booking(String guest,int room,LocalDate start,LocalDate end,double nightly){}
    static boolean overlaps(Booking a,Booking b){return a.room()==b.room()&&a.start().isBefore(b.end())&&b.start().isBefore(a.end());}
    public static void main(String[]args){var accepted=new ArrayList<Booking>();double revenue=0;for(var b:List.of(new Booking("Asha",101,LocalDate.parse("2026-09-01"),LocalDate.parse("2026-09-04"),1800),new Booking("Kabir",101,LocalDate.parse("2026-09-03"),LocalDate.parse("2026-09-05"),1800),new Booking("Riya",102,LocalDate.parse("2026-09-02"),LocalDate.parse("2026-09-04"),2200))){if(accepted.stream().anyMatch(x->overlaps(x,b))){System.out.println("rejected "+b.guest());continue;}accepted.add(b);revenue+=ChronoUnit.DAYS.between(b.start(),b.end())*b.nightly();}System.out.printf("accepted=%d revenue=%.2f%n",accepted.size(),revenue);}
}
