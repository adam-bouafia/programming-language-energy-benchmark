// The Computer Language Benchmarks Game
// https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
//
// spectral-norm benchmark in Rust

use std::env;

fn eval_a(i: usize, j: usize) -> f64 {
    1.0 / ((i + j) * (i + j + 1) / 2 + i + 1) as f64
}

fn eval_a_times_u(u: &[f64], v: &mut [f64]) {
    let n = u.len();
    for i in 0..n {
        v[i] = 0.0;
        for j in 0..n {
            v[i] += eval_a(i, j) * u[j];
        }
    }
}

fn eval_at_times_u(u: &[f64], v: &mut [f64]) {
    let n = u.len();
    for i in 0..n {
        v[i] = 0.0;
        for j in 0..n {
            v[i] += eval_a(j, i) * u[j];
        }
    }
}

fn eval_ata_times_u(u: &[f64], v: &mut [f64], w: &mut [f64]) {
    eval_a_times_u(u, w);
    eval_at_times_u(w, v);
}

fn main() {
    let n = env::args()
        .nth(1)
        .and_then(|n| n.parse().ok())
        .unwrap_or(100);
    
    let mut u = vec![1.0; n];
    let mut v = vec![0.0; n];
    let mut w = vec![0.0; n];
    
    for _ in 0..10 {
        eval_ata_times_u(&u, &mut v, &mut w);
        eval_ata_times_u(&v, &mut u, &mut w);
    }
    
    let mut vbv = 0.0;
    let mut vv = 0.0;
    
    for i in 0..n {
        vbv += u[i] * v[i];
        vv += v[i] * v[i];
    }
    
    println!("{:.9}", (vbv / vv).sqrt());
}
