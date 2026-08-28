import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Sales Commission Calculator
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    static double commission(double sales){return sales<=50000?sales*.02:sales<=100000?1000+(sales-50000)*.04:3000+(sales-100000)*.06;}
    public static void main(String[]args){double quota=90000;for(double sales:new double[]{42000,85000,125000})System.out.printf("sales=%.2f attainment=%.1f%% commission=%.2f%n",sales,sales/quota*100,commission(sales));}
}
