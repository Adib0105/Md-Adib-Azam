import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Digital Service Registry
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Request(String id,String service,String status,LocalDate opened,LocalDate closed){}
    public static void main(String[]args){var requests=List.of(new Request("R1","PAN Update","closed",LocalDate.parse("2026-08-20"),LocalDate.parse("2026-08-23")),new Request("R2","Certificate","pending",LocalDate.parse("2026-08-25"),null),new Request("R3","Bill Payment","closed",LocalDate.parse("2026-08-26"),LocalDate.parse("2026-08-26")));var counts=requests.stream().collect(Collectors.groupingBy(Request::status,Collectors.counting()));double avg=requests.stream().filter(x->x.closed()!=null).mapToLong(x->ChronoUnit.DAYS.between(x.opened(),x.closed())).average().orElse(0);System.out.printf("status=%s average_closed_days=%.1f%n",counts,avg);}
}
