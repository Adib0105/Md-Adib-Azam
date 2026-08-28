import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Text Search Engine
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    public static void main(String[]args){var docs=Map.of("d1","Java streams simplify collection processing","d2","SQL indexes improve database search","d3","Search engines build inverted indexes");var index=new TreeMap<String,Set<String>>();docs.forEach((id,text)->{for(String w:text.toLowerCase().split("\\W+"))index.computeIfAbsent(w,k->new TreeSet<>()).add(id);});for(String q:List.of("search","indexes","java"))System.out.printf("%s -> %s%n",q,index.getOrDefault(q,Set.of()));}
}
