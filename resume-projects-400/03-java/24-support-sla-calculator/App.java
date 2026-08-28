import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Support SLA Calculator
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Ticket(String id,String priority,Instant opened,Instant firstReply,Instant resolved){}
    public static void main(String[]args){var limits=Map.of("P1",60L,"P2",240L,"P3",480L);for(var t:List.of(new Ticket("T1","P1",Instant.parse("2026-08-28T10:00:00Z"),Instant.parse("2026-08-28T10:35:00Z"),Instant.parse("2026-08-28T12:00:00Z")),new Ticket("T2","P2",Instant.parse("2026-08-28T10:00:00Z"),Instant.parse("2026-08-28T15:00:00Z"),Instant.parse("2026-08-29T09:00:00Z")))){long mins=Duration.between(t.opened(),t.firstReply()).toMinutes();System.out.printf("%s first_response=%dm target=%dm met=%s resolution=%dm%n",t.id(),mins,limits.get(t.priority()),mins<=limits.get(t.priority()),Duration.between(t.opened(),t.resolved()).toMinutes());}}
}
