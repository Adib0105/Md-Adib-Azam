import java.net.URI;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Banking Console
 * Java 17 portfolio mini-project using deterministic synthetic demo data.
 */
public class App {
    record Transaction(String type,double amount){}
    public static void main(String[]args){double balance=5000;int rejected=0;
     for(var tx:List.of(new Transaction("deposit",1200),new Transaction("withdraw",850),new Transaction("withdraw",6000))){
      double delta=tx.type().equals("deposit")?tx.amount():-tx.amount();if(balance+delta<0){rejected++;continue;}balance+=delta;}
     System.out.printf("balance=%.2f rejected=%d%n",balance,rejected);
    }
}
