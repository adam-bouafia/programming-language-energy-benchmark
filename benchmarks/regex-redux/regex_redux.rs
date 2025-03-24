// The Computer Language Benchmarks Game
// https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
//
// regex-redux benchmark in Rust

use std::io::{self, Read};
use regex::Regex;

fn main() {
    // Read input
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    
    // Remove header and newlines
    let sequence = Regex::new(r">.*\n|\n").unwrap().replace_all(&input, "");
    
    // Count patterns
    let initial_length = input.len();
    let code_length = sequence.len();
    
    let patterns = [
        (r"(?i)agggtaaa|tttaccct", "agggtaaa|tttaccct"),
        (r"(?i)aggggtaaaa|tttacccct", "aggggtaaaa|tttacccct"),
        (r"(?i)agggggtaaaaa|tttaacccct", "agggggtaaaaa|tttaacccct"),
        (r"(?i)[cgt]gggtaaa|tttaccc[acg]", "[cgt]gggtaaa|tttaccc[acg]"),
        (r"(?i)a[act]ggtaaa|tttacc[agt]t", "a[act]ggtaaa|tttacc[agt]t"),
        (r"(?i)ag[act]gtaaa|tttac[agt]ct", "ag[act]gtaaa|tttac[agt]ct"),
        (r"(?i)agg[act]taaa|ttta[agt]cct", "agg[act]taaa|ttta[agt]cct"),
        (r"(?i)aggg[acg]aaa|ttt[cgt]ccct", "aggg[acg]aaa|ttt[cgt]ccct"),
        (r"(?i)agggt[cgt]aa|tt[acg]accct", "agggt[cgt]aa|tt[acg]accct"),
        (r"(?i)agggta[cgt]a|t[acg]taccct", "agggta[cgt]a|t[acg]taccct"),
        (r"(?i)agggtaa[cgt]|[acg]ttaccct", "agggtaa[cgt]|[acg]ttaccct"),
    ];
    
    for (pattern, name) in &patterns {
        let re = Regex::new(pattern).unwrap();
        let count = re.find_iter(&sequence).count();
        println!("{} {}", name, count);
    }
    
    // Perform replacements
    let result = Regex::new(r"tHa[Nt]").unwrap().replace_all(&sequence, "<4>");
    let result = Regex::new(r"aND|caN|Ha[DS]|WaS").unwrap().replace_all(&result, "<3>");
    let result = Regex::new(r"a[NSt]|BY").unwrap().replace_all(&result, "<2>");
    let result = Regex::new(r"<[^>]*>").unwrap().replace_all(&result, "|");
    let result = Regex::new(r"\|[^|][^|]*\|").unwrap().replace_all(&result, "-");
    
    println!();
    println!("{}", initial_length);
    println!("{}", code_length);
    println!("{}", result.len());
}
