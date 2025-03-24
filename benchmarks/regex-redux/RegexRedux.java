/**
 * The Computer Language Benchmarks Game
 * https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
 *
 * regex-redux benchmark in Java
 */

import java.io.*;
import java.util.*;
import java.util.regex.*;

public class RegexRedux {
    public static void main(String[] args) throws IOException {
        // Read input
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        byte[] buffer = new byte[65536];
        int count;
        while ((count = System.in.read(buffer)) > 0) {
            baos.write(buffer, 0, count);
        }
        String input = baos.toString("UTF-8");
        
        // Remove header and newlines
        String sequence = input.replaceAll(">.*\n|\n", "");
        
        // Count patterns
        int initialLength = input.length();
        int codeLength = sequence.length();
        
        Map<String, Pattern> patterns = new LinkedHashMap<>();
        patterns.put("agggtaaa|tttaccct", Pattern.compile("agggtaaa|tttaccct", Pattern.CASE_INSENSITIVE));
        patterns.put("aggggtaaaa|tttacccct", Pattern.compile("aggggtaaaa|tttacccct", Pattern.CASE_INSENSITIVE));
        patterns.put("agggggtaaaaa|tttaacccct", Pattern.compile("agggggtaaaaa|tttaacccct", Pattern.CASE_INSENSITIVE));
        patterns.put("[cgt]gggtaaa|tttaccc[acg]", Pattern.compile("[cgt]gggtaaa|tttaccc[acg]", Pattern.CASE_INSENSITIVE));
        patterns.put("a[act]ggtaaa|tttacc[agt]t", Pattern.compile("a[act]ggtaaa|tttacc[agt]t", Pattern.CASE_INSENSITIVE));
        patterns.put("ag[act]gtaaa|tttac[agt]ct", Pattern.compile("ag[act]gtaaa|tttac[agt]ct", Pattern.CASE_INSENSITIVE));
        patterns.put("agg[act]taaa|ttta[agt]cct", Pattern.compile("agg[act]taaa|ttta[agt]cct", Pattern.CASE_INSENSITIVE));
        patterns.put("aggg[acg]aaa|ttt[cgt]ccct", Pattern.compile("aggg[acg]aaa|ttt[cgt]ccct", Pattern.CASE_INSENSITIVE));
        patterns.put("agggt[cgt]aa|tt[acg]accct", Pattern.compile("agggt[cgt]aa|tt[acg]accct", Pattern.CASE_INSENSITIVE));
        patterns.put("agggta[cgt]a|t[acg]taccct", Pattern.compile("agggta[cgt]a|t[acg]taccct", Pattern.CASE_INSENSITIVE));
        patterns.put("agggtaa[cgt]|[acg]ttaccct", Pattern.compile("agggtaa[cgt]|[acg]ttaccct", Pattern.CASE_INSENSITIVE));
        
        for (Map.Entry<String, Pattern> entry : patterns.entrySet()) {
            Matcher matcher = entry.getValue().matcher(sequence);
            int count2 = 0;
            while (matcher.find()) {
                count2++;
            }
            System.out.println(entry.getKey() + " " + count2);
        }
        
        // Perform replacements
        String result = sequence;
        result = result.replaceAll("tHa[Nt]", "<4>");
        result = result.replaceAll("aND|caN|Ha[DS]|WaS", "<3>");
        result = result.replaceAll("a[NSt]|BY", "<2>");
        result = result.replaceAll("<[^>]*>", "|");
        result = result.replaceAll("\\|[^|][^|]*\\|", "-");
        
        System.out.println();
        System.out.println(initialLength);
        System.out.println(codeLength);
        System.out.println(result.length());
    }
}
