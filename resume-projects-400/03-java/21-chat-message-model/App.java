import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Chat Message Model
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Message(String sender,Instant sentAt,String text){}
    public static void main(String[]args){var messages=List.of(new Message("customer",Instant.parse("2026-08-28T10:00:00Z"),"Cannot log in"),new Message("agent",Instant.parse("2026-08-28T10:01:30Z"),"Password reset sent"),new Message("customer",Instant.parse("2026-08-28T10:03:00Z"),"Resolved, thank you"));long response=Duration.between(messages.get(0).sentAt(),messages.get(1).sentAt()).toSeconds();System.out.printf("messages=%d first_response_seconds=%d participants=%s%n",messages.size(),response,messages.stream().map(Message::sender).collect(Collectors.toSet()));}
}
