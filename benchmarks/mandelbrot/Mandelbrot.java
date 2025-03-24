/**
 * The Computer Language Benchmarks Game
 * https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
 *
 * mandelbrot benchmark in Java
 */

public class Mandelbrot {
    public static void main(String[] args) {
        int size = args.length > 0 ? Integer.parseInt(args[0]) : 200;
        
        System.out.println("P4");
        System.out.println(size + " " + size);
        
        byte[] data = new byte[(size + 7) / 8 * size];
        int dataIndex = 0;
        
        for (int y = 0; y < size; y++) {
            int bitIndex = 0;
            byte byteAcc = 0;
            
            for (int x = 0; x < size; x++) {
                double zr = 0;
                double zi = 0;
                double cr = (2.0 * x / size - 1.5);
                double ci = (2.0 * y / size - 1.0);
                double tr = 0;
                double ti = 0;
                int i = 0;
                
                for (i = 0; i < 50 && tr + ti <= 4.0; i++) {
                    zi = 2.0 * zr * zi + ci;
                    zr = tr - ti + cr;
                    tr = zr * zr;
                    ti = zi * zi;
                }
                
                byteAcc <<= 1;
                if (tr + ti <= 4.0) {
                    byteAcc |= 1;
                }
                
                bitIndex++;
                
                if (bitIndex == 8) {
                    data[dataIndex++] = byteAcc;
                    byteAcc = 0;
                    bitIndex = 0;
                } else if (x == size - 1) {
                    byteAcc <<= (8 - bitIndex);
                    data[dataIndex++] = byteAcc;
                    byteAcc = 0;
                    bitIndex = 0;
                }
            }
        }
        
        try {
            System.out.write(data);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
