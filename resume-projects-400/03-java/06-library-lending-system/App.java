import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Library Lending System
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Loan(String book,String member,LocalDate due,boolean returned){}
    public static void main(String[]args){var today=LocalDate.of(2026,8,28);var loans=List.of(new Loan("Java Basics","M1",LocalDate.of(2026,8,25),false),new Loan("SQL Guide","M2",LocalDate.of(2026,9,2),false),new Loan("Networks","M3",LocalDate.of(2026,8,20),true));
     loans.stream().filter(x->!x.returned()&&x.due().isBefore(today)).forEach(x->System.out.printf("overdue %s member=%s days=%d%n",x.book(),x.member(),ChronoUnit.DAYS.between(x.due(),today)));
    }
}
