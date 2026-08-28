import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Customer Feedback Analyzer
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Feedback(String text) {}
    public static void main(String[] args){
     var positive=Set.of("helpful","fast","resolved","good");var negative=Set.of("slow","broken","bad","late");
     var rows=List.of(new Feedback("Fast and helpful support"),new Feedback("Delivery was late and slow"));
     for(var row:rows){var words=Set.of(row.text().toLowerCase().split("\\W+"));long p=words.stream().filter(positive::contains).count(),n=words.stream().filter(negative::contains).count();
     System.out.printf("%s => %s (positive=%d negative=%d)%n",row.text(),p>n?"positive":n>p?"negative":"neutral",p,n);}
    }
}
