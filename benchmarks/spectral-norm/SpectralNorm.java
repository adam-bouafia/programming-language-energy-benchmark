/**
 * The Computer Language Benchmarks Game
 * https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
 *
 * spectral-norm benchmark in Java
 */

public class SpectralNorm {
    private static final int DEFAULT_N = 100;

    private static double eval_A(int i, int j) {
        return 1.0 / ((i + j) * (i + j + 1) / 2 + i + 1);
    }

    private static void eval_A_times_u(double[] u, double[] v) {
        for (int i = 0; i < u.length; i++) {
            v[i] = 0;
            for (int j = 0; j < u.length; j++) {
                v[i] += eval_A(i, j) * u[j];
            }
        }
    }

    private static void eval_At_times_u(double[] u, double[] v) {
        for (int i = 0; i < u.length; i++) {
            v[i] = 0;
            for (int j = 0; j < u.length; j++) {
                v[i] += eval_A(j, i) * u[j];
            }
        }
    }

    private static void eval_AtA_times_u(double[] u, double[] v, double[] w) {
        eval_A_times_u(u, w);
        eval_At_times_u(w, v);
    }

    public static void main(String[] args) {
        int n = args.length > 0 ? Integer.parseInt(args[0]) : DEFAULT_N;

        double[] u = new double[n];
        double[] v = new double[n];
        double[] w = new double[n];

        for (int i = 0; i < n; i++) {
            u[i] = 1.0;
        }

        for (int i = 0; i < 10; i++) {
            eval_AtA_times_u(u, v, w);
            eval_AtA_times_u(v, u, w);
        }

        double vBv = 0.0;
        double vv = 0.0;

        for (int i = 0; i < n; i++) {
            vBv += u[i] * v[i];
            vv += v[i] * v[i];
        }

        System.out.printf("%.9f\n", Math.sqrt(vBv / vv));
    }
}
