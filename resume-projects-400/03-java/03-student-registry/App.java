import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Student Registry
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Student(int id,String name,List<Integer> marks){double average(){return marks.stream().mapToInt(Integer::intValue).average().orElse(0);}}
    public static void main(String[]args){var students=new ArrayList<>(List.of(new Student(1,"Asha",List.of(84,91,88)),new Student(2,"Kabir",List.of(72,79,81)),new Student(3,"Riya",List.of(93,95,90))));
     students.sort(Comparator.comparingDouble(Student::average).reversed());students.forEach(s->System.out.printf("%s %.1f%n",s.name(),s.average()));
    }
}
