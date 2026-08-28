import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Quiz Application
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Question(String id,String answer,String explanation){}
    public static void main(String[]args){var questions=List.of(new Question("q1","B","Lists are mutable"),new Question("q2","A","SELECT reads rows"),new Question("q3","C","HTTP 404 means not found"));var answers=Map.of("q1","B","q2","C","q3","C");int score=0;for(var q:questions){boolean ok=q.answer().equals(answers.get(q.id()));if(ok)score++;System.out.printf("%s %s - %s%n",q.id(),ok?"correct":"incorrect",q.explanation());}System.out.printf("score=%d/%d%n",score,questions.size());}
}
