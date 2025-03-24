/**
 * The Computer Language Benchmarks Game
 * https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
 *
 * binary-trees benchmark in Java
 */

class BinaryTrees {
    private static class Node {
        Node left, right;
        int item;

        Node(int item) {
            this.item = item;
        }

        Node(int item, Node left, Node right) {
            this.item = item;
            this.left = left;
            this.right = right;
        }
    }

    private static Node makeTree(int depth) {
        if (depth <= 0) {
            return new Node(0);
        }
        return new Node(depth, makeTree(depth - 1), makeTree(depth - 1));
    }

    private static int checkTree(Node node) {
        if (node.left == null) {
            return node.item;
        }
        return node.item + checkTree(node.left) - checkTree(node.right);
    }

    public static void main(String[] args) {
        int n = args.length > 0 ? Integer.parseInt(args[0]) : 10;
        int minDepth = 4;
        int maxDepth = Math.max(minDepth + 2, n);

        // Create and check stretch tree
        int stretchDepth = maxDepth + 1;
        Node stretchTree = makeTree(stretchDepth);
        System.out.println("stretch tree of depth " + stretchDepth + "\t check: " + checkTree(stretchTree));

        // Create long-lived tree
        Node longLivedTree = makeTree(maxDepth);

        // Create, check, and delete multiple trees
        for (int depth = minDepth; depth <= maxDepth; depth += 2) {
            int iterations = 1 << (maxDepth - depth + minDepth);
            int check = 0;

            for (int i = 1; i <= iterations; i++) {
                Node tempTree = makeTree(depth);
                check += checkTree(tempTree);
            }

            System.out.println(iterations + "\t trees of depth " + depth + "\t check: " + check);
        }

        // Check long-lived tree
        System.out.println("long lived tree of depth " + maxDepth + "\t check: " + checkTree(longLivedTree));
    }
}
