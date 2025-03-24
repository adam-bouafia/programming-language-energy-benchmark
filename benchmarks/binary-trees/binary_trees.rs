// The Computer Language Benchmarks Game
// https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
//
// binary-trees benchmark in Rust

use std::env;

struct Node {
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
    item: i32,
}

impl Node {
    fn new(item: i32) -> Self {
        Node {
            left: None,
            right: None,
            item,
        }
    }

    fn new_with_children(item: i32, left: Node, right: Node) -> Self {
        Node {
            left: Some(Box::new(left)),
            right: Some(Box::new(right)),
            item,
        }
    }

    fn check(&self) -> i32 {
        match (&self.left, &self.right) {
            (None, None) => self.item,
            (Some(left), Some(right)) => self.item + left.check() - right.check(),
            _ => unreachable!(),
        }
    }
}

fn make_tree(depth: i32) -> Node {
    if depth <= 0 {
        return Node::new(0);
    }
    Node::new_with_children(depth, make_tree(depth - 1), make_tree(depth - 1))
}

fn main() {
    let n = env::args()
        .nth(1)
        .and_then(|n| n.parse().ok())
        .unwrap_or(10);
    let min_depth = 4;
    let max_depth = if min_depth + 2 > n { min_depth + 2 } else { n };

    // Create and check stretch tree
    let stretch_depth = max_depth + 1;
    let stretch_tree = make_tree(stretch_depth);
    println!(
        "stretch tree of depth {}\t check: {}",
        stretch_depth,
        stretch_tree.check()
    );

    // Create long-lived tree
    let long_lived_tree = make_tree(max_depth);

    // Create, check, and delete multiple trees
    for depth in (min_depth..=max_depth).step_by(2) {
        let iterations = 1 << (max_depth - depth + min_depth);
        let mut check = 0;

        for _ in 1..=iterations {
            let temp_tree = make_tree(depth);
            check += temp_tree.check();
        }

        println!("{}\t trees of depth {}\t check: {}", iterations, depth, check);
    }

    // Check long-lived tree
    println!(
        "long lived tree of depth {}\t check: {}",
        max_depth,
        long_lived_tree.check()
    );
}
