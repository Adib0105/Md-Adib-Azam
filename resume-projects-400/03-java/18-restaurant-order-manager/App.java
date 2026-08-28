import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Restaurant Order Manager
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record OrderLine(String item,int qty,double price){}
    public static void main(String[]args){var order=List.of(new OrderLine("Biryani",3,240),new OrderLine("Cold Drink",3,40),new OrderLine("Dessert",2,80));double subtotal=order.stream().mapToDouble(x->x.qty()*x.price()).sum(),gst=subtotal*.05,service=subtotal*.03;order.forEach(x->System.out.printf("%s x%d = %.2f%n",x.item(),x.qty(),x.qty()*x.price()));System.out.printf("subtotal=%.2f gst=%.2f service=%.2f total=%.2f%n",subtotal,gst,service,subtotal+gst+service);}
}
