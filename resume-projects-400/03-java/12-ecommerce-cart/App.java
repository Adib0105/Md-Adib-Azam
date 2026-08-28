import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Ecommerce Cart
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Line(String sku,int quantity,double unitPrice){}
    public static void main(String[]args){var lines=List.of(new Line("A1",2,799),new Line("B2",1,1299));double subtotal=lines.stream().mapToDouble(x->x.quantity()*x.unitPrice()).sum(),discount=subtotal>=2500?subtotal*.10:0,tax=(subtotal-discount)*.18,shipping=subtotal-discount>=2000?0:99;System.out.printf("subtotal=%.2f discount=%.2f tax=%.2f shipping=%.2f total=%.2f%n",subtotal,discount,tax,shipping,subtotal-discount+tax+shipping);}
}
