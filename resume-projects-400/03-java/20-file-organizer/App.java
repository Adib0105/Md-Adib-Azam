import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * File Organizer
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    public static void main(String[]args){var files=List.of("resume.pdf","photo.JPG","data.csv","README");var plan=new TreeMap<String,List<String>>();for(String file:files){int dot=file.lastIndexOf('.');String ext=dot<0?"no-extension":file.substring(dot+1).toLowerCase();plan.computeIfAbsent(ext,k->new ArrayList<>()).add(file);}plan.forEach((folder,names)->System.out.printf("%s -> %s%n",folder,names));System.out.println("dry_run=true");}
}
