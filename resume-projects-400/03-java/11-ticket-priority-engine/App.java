import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Ticket Priority Engine
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Ticket(String id,boolean blocked,int users,long ageHours){}
    static int score(Ticket t){return (t.blocked()?50:0)+Math.min(t.users()*3,30)+(int)Math.min(t.ageHours(),20);}
    public static void main(String[]args){var tickets=new ArrayList<>(List.of(new Ticket("T1",true,12,2),new Ticket("T2",false,2,48),new Ticket("T3",true,1,1)));tickets.sort(Comparator.comparingInt(App::score).reversed());tickets.forEach(t->System.out.printf("%s score=%d priority=%s%n",t.id(),score(t),score(t)>=70?"P1":score(t)>=40?"P2":"P3"));}
}
