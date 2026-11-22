package main.java;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Random;

public class ExperimentRunner {

    private static final int[] SIZES = {10_000, 50_000, 100_000, 500_000};
    private static final int[] CUTOFFS = {0, 3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 17, 20, 25, 30};
    private static final String[] TYPES = {"random", "nearly_sorted", "few_unique"};
    private static final int WARMUP_RUNS = 3;
    private static final int MEASURED_RUNS = 7;
    private static final long SEED = 777777L;

    public static void main(String[] args) throws IOException {
        File outDir = new File("out");
        if (!outDir.exists()) {
            outDir.mkdirs();
        }
        File resultsDir = new File("results");
        if (!resultsDir.exists()) {
            resultsDir.mkdirs();
        }

        Random rng = new Random(SEED);
        String csvPath = "results/cutoff_results.csv";

        try (PrintWriter writer = new PrintWriter(new FileWriter(csvPath))) {
            writer.println("type,n,cutoff,avg_time_ms");

            for (String type : TYPES) {
                for (int n : SIZES) {
                    Integer[] baseData = generateData(type, n, rng);

                    for (int cutoff : CUTOFFS) {
                        for (int w = 0; w < WARMUP_RUNS; w++) {
                            Integer[] copy = baseData.clone();
                            MergeCutoff.sort(copy, cutoff);
                        }

                        long totalNs = 0L;
                        for (int r = 0; r < MEASURED_RUNS; r++) {
                            Integer[] copy = baseData.clone();
                            long start = System.nanoTime();
                            MergeCutoff.sort(copy, cutoff);
                            long elapsed = System.nanoTime() - start;
                            totalNs += elapsed;

                            if (!MergeCutoff.isSorted(copy)) {
                                throw new IllegalStateException("Array not sorted for cutoff=" + cutoff);
                            }
                        }

                        double avgMs = (totalNs / (double) MEASURED_RUNS) / 1_000_000.0;
                        writer.printf(java.util.Locale.US, "%s,%d,%d,%.4f%n", type, n, cutoff, avgMs);
                        System.out.printf("Done | type=%-13s | N=%-6d | cutoff=%-2d | avg=%.4f ms%n",
                                type, n, cutoff, avgMs);
                    }
                }
            }
        }

        System.out.println("Saved benchmark results to " + csvPath);
    }

    private static Integer[] generateData(String type, int n, Random rng) {
        Integer[] arr = new Integer[n];
        if ("random".equals(type)) {
            for (int i = 0; i < n; i++) {
                arr[i] = rng.nextInt(n * 10);
            }
        } else if ("nearly_sorted".equals(type)) {
            for (int i = 0; i < n; i++) {
                arr[i] = i;
            }
            int swaps = Math.max(1, n / 100);
            for (int s = 0; s < swaps; s++) {
                int i = rng.nextInt(n);
                int j = rng.nextInt(n);
                int tmp = arr[i];
                arr[i] = arr[j];
                arr[j] = tmp;
            }
        } else if ("few_unique".equals(type)) {
            int bound = Math.max(2, Math.min(50, n / 10));
            for (int i = 0; i < n; i++) {
                arr[i] = rng.nextInt(bound);
            }
        }
        return arr;
    }
}
