import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Password Policy Validator
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    static List<String> issues(String password){var out=new ArrayList<String>();if(password.length()<12)out.add("minimum 12 characters");if(!password.matches(".*[A-Z].*"))out.add("uppercase");if(!password.matches(".*[a-z].*"))out.add("lowercase");if(!password.matches(".*\\d.*"))out.add("digit");if(!password.matches(".*[^A-Za-z0-9].*"))out.add("symbol");if(password.toLowerCase().contains("password"))out.add("forbidden term");return out;}
    public static void main(String[]args){for(String p:List.of("weak","Adib#Portfolio2026"))System.out.printf("length=%d valid=%s issues=%s%n",p.length(),issues(p).isEmpty(),issues(p));}
}
