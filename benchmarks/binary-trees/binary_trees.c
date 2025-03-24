/**
 * The Computer Language Benchmarks Game
 * https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
 *
 * binary-trees benchmark in C
 */

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

typedef struct tree_node {
    struct tree_node* left;
    struct tree_node* right;
    int item;
} tree_node;

tree_node* make_tree(int depth) {
    tree_node* node = malloc(sizeof(tree_node));
    
    if (depth > 0) {
        node->left = make_tree(depth - 1);
        node->right = make_tree(depth - 1);
        node->item = depth;
    } else {
        node->left = NULL;
        node->right = NULL;
        node->item = 0;
    }
    
    return node;
}

int check_tree(tree_node* node) {
    if (node->left == NULL)
        return node->item;
    else
        return node->item + check_tree(node->left) - check_tree(node->right);
}

void delete_tree(tree_node* node) {
    if (node->left != NULL) {
        delete_tree(node->left);
        delete_tree(node->right);
    }
    free(node);
}

int main(int argc, char* argv[]) {
    int n = argc > 1 ? atoi(argv[1]) : 10;
    int min_depth = 4;
    int max_depth = n < min_depth + 2 ? min_depth + 2 : n;
    
    // Create and check stretch tree
    int stretch_depth = max_depth + 1;
    tree_node* stretch_tree = make_tree(stretch_depth);
    printf("stretch tree of depth %d\t check: %d\n", 
           stretch_depth, check_tree(stretch_tree));
    delete_tree(stretch_tree);
    
    // Create long-lived tree
    tree_node* long_lived_tree = make_tree(max_depth);
    
    // Create, check, and delete multiple trees
    for (int depth = min_depth; depth <= max_depth; depth += 2) {
        int iterations = 1 << (max_depth - depth + min_depth);
        int check = 0;
        
        for (int i = 1; i <= iterations; i++) {
            tree_node* temp_tree = make_tree(depth);
            check += check_tree(temp_tree);
            delete_tree(temp_tree);
        }
        
        printf("%d\t trees of depth %d\t check: %d\n", 
               iterations, depth, check);
    }
    
    // Check and delete long-lived tree
    printf("long lived tree of depth %d\t check: %d\n", 
           max_depth, check_tree(long_lived_tree));
    delete_tree(long_lived_tree);
    
    return 0;
}
