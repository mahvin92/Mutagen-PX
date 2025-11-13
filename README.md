# Mutagen-PX

## About
Mutagen-PX is a lightweight Python toolkit that simulates tumor-specific gene sequence profiles by applying patient mutation data from TCGA cohorts to a reference sequence.  
It recreates “mutated” FASTA outputs per patient, allowing comparative genomics and downstream mutational analyses.

---

## Overview

Mutagen-PX takes:
1. A text file of a reference gene sequence (in FASTA format)
```
Sample format:
>NC_000017.11:c7668421-7687490 Homo sapiens chromosome 17, GRCh38.p14 Primary Assembly
CTCAAAAGTCTAGAGCCACCGTCCAGGGAGCAGGTAGCTGCTGGGCTCCGGGGACACTTTGCGTTCGGGC
TGGGAGCGTGCTTTCCACGACGGTGACACGCTTCCCTGGATTGGGTAAGCTCCTGACTGAACTTGATGAG
TCCTCTCTGAGTCACGGGCTCTCGGCTCCGTGTATTTTCAGCTCGGGAAAATCGCTGGGGCTGGGGGTGG
GGCAGTGGGGACTTAGCGAGTTTGGGGGTGAGTGGGATGGAAGCTTGGCTAGAGGGATCATCATAGGAGT
TGCATTGTTGGGAGACCTGGGTGTAGATGATGGGGATGTTAGGACCATCCGAACTCAAAGTTGAACGCCT
AGGCAGAGGAGTGGAGCTTTGGGGAACCTTGAGCCGGCCTAAAGCGTACTTCTTTGCACATCCACCCGGT
GCTGGGCGTAGGGAATCCCTGAAATAAAAGATGCACAAAGCATTGAGGTCTGAGACTTTTGGATCTCGAA
ACATTGAGAACTCATAGCTGTATATTTTAGAGCCCATGGCATCCTAGTGAAAACTGGGGCTCCATTCCGA
AATGATCATTTGGGGGTGATCCGGGGAGCCCAAGCTGCTAAGGTCCCACAACTTCCGGACCTTTGTCCTT
```

2. A mutation table derived from TCGA (TSV format)

| sample | gene start | gene end | reference | change |
|--------|-------------|-----------|------------|---------|
| TCGA-01 | 215 | 215 | G | T |
| TCGA-02 | 500 | 502 | - | AGT |
| TCGA-03 | no variant | no variant | no variant | no variant |


It then:
- Parses each patient's variant data,
- Applies point mutations, insertions, or deletions to the reference sequence,
- Outputs a **multi-FASTA file** containing patient-specific mutated sequences.

## Sample results
>reference seq
ATGCGTACGTTAGCA

```
>TCGA-01 | start:3 | end:3 | ref:G | change:A
ATACGTACGTTAGCA
>TCGA-02 | start:1 | end:1 | ref:A | change:C
CTGCGTACGTTAGCA
>TCGA-03 | start:7 | end:7 | ref:A | change:-
ATGCGTCGTTAGCA
>TCGA-04 | start:9 | end:9 | ref:G | change:T
ATGCGTACTTTAGCA
>TCGA-05 | start:2 | end:2 | ref:T | change:G
AGGCGTACGTTAGCA
>TCGA-06 | start:4 | end:6 | ref:CGT | change:- 
ATGACGTTAGCA
>TCGA-07 | start:1 | end:1 | ref:A | change:GGGA
GGGATGCGTACGTTAGCC
```

## Run locally
1. Intall pandas
```pip install pandas```

2. Run Mutagen-PX
```
mutagen-px.py --gene GENE_NAME --ref REF_SEQ_TXT --profile MUTATION_PROFILE_TSV --outdir DIRECTORY
```
Sample script: ```mutagen-px.py --gene TP53 --ref ref_seq.txt --profile patient_profile.tsv --outdir output```

*The script above assumes that the sequence name is TP53, the TP53 ref seq (FASTA format) is locate in ref_seq.txt file, the mutational profiles of patients are in patient_profile.tsv, and the run will generate a subdirectory named 'output'. The output folder will contain the multi-FASTA result.*

## Run on Colab
Load the [notebook](https://github.com/mahvin92/Mutagen-PX) to Colab and run all the cells.

## Reporting
Comments and suggestions to improve Mutagen-PX are welcome. If you find any bug or problem, please open an issue.

## Acknowledgement
Designed with love by Marvin 😉
