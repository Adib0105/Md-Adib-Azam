import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Attendance Tracker
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Student(String name,String pattern){}
    public static void main(String[]args){for(var s:List.of(new Student("Asha","PPAPPPPP"),new Student("Kabir","PAAAPAPP"))){long present=s.pattern().chars().filter(c->c=='P').count();double pct=100.0*present/s.pattern().length();boolean streak=s.pattern().contains("AAA");System.out.printf("%s attendance=%.1f%% eligible=%s absence_risk=%s%n",s.name(),pct,pct>=75,streak);}}
}
