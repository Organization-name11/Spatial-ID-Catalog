import java.io.*;
import java.net.*;
import java.util.*;
import com.fasterxml.jackson.databind.*;

public class GitHubSpatialIdFetcher {

    static final String TOKEN = "YOUR_GITHUB_TOKEN";
    static final String QUERY = "空間ID OR spatial-id OR spatialid";

    public static void main(String[] args) throws Exception {
        List<Map<String, Object>> results = new ArrayList<>();

        String url = "https://api.github.com/search/repositories?q=" +
                URLEncoder.encode(QUERY, "UTF-8") +
                "&per_page=100";

        HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
        conn.setRequestProperty("Authorization", "Bearer " + TOKEN);
        conn.setRequestProperty("Accept", "application/vnd.github+json");

        ObjectMapper mapper = new ObjectMapper();
        JsonNode root = mapper.readTree(conn.getInputStream());
        JsonNode items = root.get("items");

        for (JsonNode item : items) {
            Map<String, Object> repo = new LinkedHashMap<>();
            repo.put("name", item.get("full_name").asText());
            repo.put("url", item.get("html_url").asText());
            repo.put("description", item.get("description").isNull() ? "" : item.get("description").asText());
            repo.put("stars", item.get("stargazers_count").asInt());

            // topics取得
            List<String> topics = new ArrayList<>();
            if (item.has("topics")) {
                for (JsonNode t : item.get("topics")) {
                    topics.add(t.asText());
                }
            }
            repo.put("topics", topics);

            results.add(repo);
        }

        mapper.writerWithDefaultPrettyPrinter()
              .writeValue(new File("repos.json"), results);

        System.out.println("repos.json generated: " + results.size());
    }
}
