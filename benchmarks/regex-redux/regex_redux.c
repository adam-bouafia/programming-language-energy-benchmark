/**
 * The Computer Language Benchmarks Game
 * https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
 *
 * regex-redux benchmark in C
 * contributed by Jeremy Zerfas
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pcre.h>

#define VARIANTS_LENGTH 9
#define SUBSTITUTIONS_LENGTH 5

int main(int argc, char ** argv){
    // Read input file or stdin
    FILE * input_file;
    if(argc > 1)
        input_file=fopen(argv[1], "r");
    else
        input_file=stdin;

    // Get file size
    fseek(input_file, 0, SEEK_END);
    const size_t file_size=ftell(input_file);
    fseek(input_file, 0, SEEK_SET);

    // Read file into memory
    char * const original_sequence=malloc(file_size+1);
    size_t bytes_read=fread(original_sequence, 1, file_size, input_file);
    original_sequence[bytes_read]='\0';
    fclose(input_file);

    // Skip initial description
    char * sequence=strstr(original_sequence, ">THREE");
    sequence=strchr(sequence, '\n')+1;

    // Remove newlines
    pcre * pattern=pcre_compile("\\n", 0, NULL, NULL, NULL);
    pcre_extra * pattern_extra=pcre_study(pattern, 0, NULL);
    
    char * new_sequence=malloc(file_size+1);
    pcre_exec(pattern, pattern_extra, sequence, strlen(sequence), 0, 0, NULL, 0);
    pcre_copy_substring(sequence, NULL, 0, 0, new_sequence, file_size+1);
    
    free(original_sequence);
    sequence=new_sequence;

    // Count pattern matches
    const char * const variants[VARIANTS_LENGTH]={
        "agggtaaa|tttaccct",
        "[cgt]gggtaaa|tttaccc[acg]",
        "a[act]ggtaaa|tttacc[agt]t",
        "ag[act]gtaaa|tttac[agt]ct",
        "agg[act]taaa|ttta[agt]cct",
        "aggg[acg]aaa|ttt[cgt]ccct",
        "agggt[cgt]aa|tt[acg]accct",
        "agggta[cgt]a|t[acg]taccct",
        "agggtaa[cgt]|[acg]ttaccct"
    };

    for(int i=0; i<VARIANTS_LENGTH; i++){
        pattern=pcre_compile(variants[i], 0, NULL, NULL, NULL);
        pattern_extra=pcre_study(pattern, 0, NULL);
        
        int count=0;
        int offset=0;
        int ovector[30];
        
        while(pcre_exec(pattern, pattern_extra, sequence, strlen(sequence), offset, 0, ovector, 30) >= 0){
            count++;
            offset=ovector[1];
        }
        
        printf("%s %d\n", variants[i], count);
        
        pcre_free(pattern);
        pcre_free_study(pattern_extra);
    }

    // Perform substitutions
    const char * const substitutions[SUBSTITUTIONS_LENGTH][2]={
        {"tHa[Nt]", "<4>"},
        {"aND|cAN|Ha[DS]|WaS", "<3>"},
        {"a[NSt]|BY", "<2>"},
        {"<[^>]*>", "|"},
        {"\\|[^|][^|]*\\|", "-"}
    };

    for(int i=0; i<SUBSTITUTIONS_LENGTH; i++){
        pattern=pcre_compile(substitutions[i][0], 0, NULL, NULL, NULL);
        pattern_extra=pcre_study(pattern, 0, NULL);
        
        char * result=malloc(file_size+1);
        pcre_exec(pattern, pattern_extra, sequence, strlen(sequence), 0, 0, NULL, 0);
        pcre_copy_substring(sequence, NULL, 0, 0, result, file_size+1);
        
        free(sequence);
        sequence=result;
        
        pcre_free(pattern);
        pcre_free_study(pattern_extra);
    }

    printf("\nLength before: %zu\n", strlen(new_sequence));
    printf("Length after: %zu\n", strlen(sequence));

    free(sequence);
    
    return 0;
}
