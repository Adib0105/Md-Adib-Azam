import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * URL Validator
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    public static void main(String[]args){for(String raw:List.of("https://example.com/path","ftp://example.com","not a url")){boolean valid=false;String reason="invalid syntax";try{var uri=URI.create(raw);valid=Set.of("http","https").contains(uri.getScheme())&&uri.getHost()!=null;reason=valid?"ok":"requires http(s) and host";}catch(IllegalArgumentException ignored){}System.out.printf("%s valid=%s reason=%s%n",raw,valid,reason);}}
}
