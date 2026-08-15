import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class FeedbackAnalyzer {
    record Feedback(String id, int rating, String comment) {}

    static String sentiment(Feedback feedback) {
        String text = feedback.comment().toLowerCase(Locale.ROOT);
        String[] positive = {"helpful", "quick", "good", "excellent", "resolved"};
        String[] negative = {"slow", "bad", "confusing", "frustrated", "unresolved"};
        int score = feedback.rating() >= 4 ? 1 : feedback.rating() <= 2 ? -1 : 0;
        for (String word : positive) if (text.contains(word)) score++;
        for (String word : negative) if (text.contains(word)) score--;
        return score > 0 ? "positive" : score < 0 ? "negative" : "neutral";
    }

    static List<Feedback> load(Path path) throws IOException {
        List<Feedback> rows = new ArrayList<>();
        try (BufferedReader reader = Files.newBufferedReader(path)) {
            reader.readLine();
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",", 3);
                if (parts.length != 3) continue;
                try {
                    rows.add(new Feedback(parts[0], Integer.parseInt(parts[1]), parts[2]));
                } catch (NumberFormatException ignored) {
                    // Skip malformed rows while keeping the report available.
                }
            }
        }
        return rows;
    }

    static void report(List<Feedback> rows) {
        int positive = 0, neutral = 0, negative = 0, ratingTotal = 0;
        for (Feedback feedback : rows) {
            ratingTotal += feedback.rating();
            switch (sentiment(feedback)) {
                case "positive" -> positive++;
                case "negative" -> negative++;
                default -> neutral++;
            }
        }
        double average = rows.isEmpty() ? 0.0 : (double) ratingTotal / rows.size();
        System.out.println("Customer feedback report");
        System.out.printf(Locale.ROOT, "Responses: %d%nAverage rating: %.2f%n", rows.size(), average);
        System.out.printf("Positive: %d%nNeutral: %d%nNegative: %d%n", positive, neutral, negative);
    }

    public static void main(String[] args) throws IOException {
        if (args.length != 1) {
            System.err.println("Usage: java FeedbackAnalyzer.java feedback.csv");
            System.exit(1);
        }
        report(load(Path.of(args[0])));
    }
}
