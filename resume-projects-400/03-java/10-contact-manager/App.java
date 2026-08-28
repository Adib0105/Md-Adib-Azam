import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Contact Manager
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Contact(String name,String phone,String email){}
    public static void main(String[]args){var seen=new HashSet<String>();var clean=new ArrayList<Contact>();for(var c:List.of(new Contact(" Adib ","+91 94332 80105","A@EXAMPLE.COM"),new Contact("Adib","919433280105","a@example.com"),new Contact("Riya","9999999999","bad-email"))){String phone=c.phone().replaceAll("\\D",""),email=c.email().toLowerCase();if(seen.add(phone)&&email.matches("^[^@]+@[^@]+\\.[^@]+$"))clean.add(new Contact(c.name().trim(),phone,email));}clean.forEach(System.out::println);}
}
