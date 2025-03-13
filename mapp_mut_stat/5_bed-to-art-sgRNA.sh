#!/bin/bash

python mpmat-to-art-sgRNA.py \
        -i {sample1}.sorted.bam.read1.bam.mut.stat.nonSNP.merge.rmbakeground.bed \
        -q GAGTCCGAGCAGAAGAAGAANRG \ #sgRNA target sequence
        --input_filetype bed \
        -r /home/UCSC/hg38.fa \
        -o {sample1}.sorted.bam.read1.bam.mut.stat.nonSNP.merge.rmbakeground.bed.art \
        -m region \
        -e 50 \
        --input_header False \
        --mpmat_fwd_mut_type AG \
        --mpmat_rev_mut_type TC \
        --seed_index 15,20 \
        --align_settings 5,-4,-24,-8 \
        --PAM_type_penalty 0,8,12 \
        --dna_bulge_penalty 24,8 \
        --rna_bulge_penalty 24,8 \
        --dna_bulge_cmp_weight 1,24 \
        --rna_bulge_cmp_weight 1,24 \
        --mismatch_cmp_weight 10,2 \
        --dist_to_signal_penalty_k 0,0,0,0,0,0 \
        --dist_to_signal_penalty_offset 12,0,0,0,0,12 \
        --align_step_window_size 23 \
        --align_step_move_size 1


