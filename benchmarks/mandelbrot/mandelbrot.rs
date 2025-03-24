// The Computer Language Benchmarks Game
// https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
//
// mandelbrot benchmark in Rust

use std::env;
use std::io::{self, Write};

fn main() {
    let size = env::args()
        .nth(1)
        .and_then(|n| n.parse().ok())
        .unwrap_or(200);
    
    println!("P4");
    println!("{} {}", size, size);
    
    let mut data = vec![0u8; (size + 7) / 8 * size];
    let mut data_index = 0;
    
    for y in 0..size {
        let mut bit_index = 0;
        let mut byte_acc = 0;
        
        for x in 0..size {
            let mut zr = 0.0;
            let mut zi = 0.0;
            let cr = 2.0 * x as f64 / size as f64 - 1.5;
            let ci = 2.0 * y as f64 / size as f64 - 1.0;
            let mut tr = 0.0;
            let mut ti = 0.0;
            
            let mut i = 0;
            while i < 50 && tr + ti <= 4.0 {
                zi = 2.0 * zr * zi + ci;
                zr = tr - ti + cr;
                tr = zr * zr;
                ti = zi * zi;
                i += 1;
            }
            
            byte_acc <<= 1;
            if tr + ti <= 4.0 {
                byte_acc |= 1;
            }
            
            bit_index += 1;
            
            if bit_index == 8 {
                data[data_index] = byte_acc;
                data_index += 1;
                byte_acc = 0;
                bit_index = 0;
            } else if x == size - 1 {
                byte_acc <<= (8 - bit_index);
                data[data_index] = byte_acc;
                data_index += 1;
                byte_acc = 0;
                bit_index = 0;
            }
        }
    }
    
    io::stdout().write_all(&data).unwrap();
}
