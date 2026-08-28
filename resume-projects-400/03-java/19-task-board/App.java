import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Task Board
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Task(String title,String status,String owner){}
    public static void main(String[]args){var tasks=List.of(new Task("API","Doing","Adib"),new Task("Tests","Doing","Asha"),new Task("Docs","Doing","Riya"),new Task("Deploy","Todo","Adib"),new Task("Review","Done","Kabir"));var board=tasks.stream().collect(Collectors.groupingBy(Task::status,LinkedHashMap::new,Collectors.toList()));board.forEach((k,v)->System.out.printf("%s (%d): %s%n",k,v.size(),v.stream().map(Task::title).toList()));System.out.println("wip_breach="+(board.getOrDefault("Doing",List.of()).size()>2));}
}
