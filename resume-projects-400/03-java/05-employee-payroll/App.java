import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Employee Payroll
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Employee(String name,double basic,double allowance,double overtime){}
    static double tax(double gross){return gross<=25000?0:gross<=50000?(gross-25000)*.10:2500+(gross-50000)*.20;}
    public static void main(String[]args){for(var e:List.of(new Employee("Asha",42000,8000,2500),new Employee("Kabir",24000,4000,0))){double gross=e.basic()+e.allowance()+e.overtime(),t=tax(gross);System.out.printf("%s gross=%.2f tax=%.2f net=%.2f%n",e.name(),gross,t,gross-t);}}
}
