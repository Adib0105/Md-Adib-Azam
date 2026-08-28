import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Inventory Service
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Item(String sku,int quantity,int reorder,int target,double cost){}
    public static void main(String[]args){var items=List.of(new Item("A1",4,5,20,80),new Item("B2",15,8,25,120));double value=items.stream().mapToDouble(x->x.quantity()*x.cost()).sum();
     items.stream().filter(x->x.quantity()<=x.reorder()).forEach(x->System.out.printf("reorder %s qty=%d%n",x.sku(),x.target()-x.quantity()));System.out.printf("value=%.2f%n",value);
    }
}
