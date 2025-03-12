#!/usr/bin/env runsnakemake
configfile: "config.yaml"

samples = config["samples"]
threads = config["threads"]
bowtie2_index = config["bowtie2_index"]
indir = config["path"]
outdir = "results"

rule all:
	input:
		expand(outdir + "/bam/{sample}.sorted.bam", sample = samples),
		expand(outdir + "/bam/{sample}.sorted.bam.bai", sample = samples),
		expand(outdir + "/bam/{sample}.picard.bam", sample = samples),
		expand(outdir + "/bam/{sample}.picard.bam.bai", sample = samples),
		expand(outdir + "/read1/{sample}.picard.bam.read1.bam", sample = samples),
		expand(outdir + "/read1/{sample}.picard.bam.read1.bam.bai", sample = samples),
#		expand(outdir + "/read1/{sample}.picard.bam.read1.bam", sample = samples),
#		expand(outdir + "/read1/{sample}.picard.bam.read1.bam.bai", sample = samples),

rule trim_galore:
	input:
		indir + "/fq/{sample}_1.fq.gz",
		indir + "/fq/{sample}_2.fq.gz"
	output:
		outdir + "/clean_fq/{sample}_1_val_1.fq.gz",
		outdir + "/clean_fq/{sample}_2_val_2.fq.gz"
	params:
		outdir + "/clean_fq"
	threads:
		threads
	shell:
		"trim_galore -j {threads} --quality 20 --phred33 --stringency 3 --length 16 -o {params} --paired {input}"

rule bwa_mapping:
	input:
		fq1 = outdir + "/clean_fq/{sample}_1_val_1.fq.gz",
		fq2 = outdir + "/clean_fq/{sample}_2_val_2.fq.gz"
#		fq1 = indir + "/fq/{sample}_1.fq.gz",
#		fq2 = indir + "/fq/{sample}_2.fq.gz"
	output:
		temp(outdir + "/bam/{sample}.sam")
	threads:
		threads
	log:
		outdir + "/bam/logs/{sample}.log"
	shell:
		"bowtie2 -p {threads} --end-to-end -x {bowtie2_index} -1 {input.fq1} -2 {input.fq2} -S {output} 2> {log}"

rule samtools_sam2bam:
	input:
		outdir + "/bam/{sample}.sam"
	output:
		temp(outdir + "/bam/{sample}.bam")
	threads:
		threads
	shell:
		"samtools view -@ {threads} -bS -f 3 -q 5 {input} > {output}"

rule bam_sort:
	input:
		outdir + "/bam/{sample}.bam"
	output:
		outdir + "/bam/{sample}.sorted.bam"
	threads:
		threads
	shell:
		"samtools sort -@ {threads} -o {output} {input}"

rule picard:
	input:
		outdir + "/bam/{sample}.sorted.bam"
	output:
		outdir + "/bam/{sample}.picard.bam"
	params:
		outdir + "/bam/{sample}.picard.bam.markdup.matrix"
	shell:
		"picard MarkDuplicates --REMOVE_DUPLICATES  -I {input} -O {output} -M {params}"

rule bam_index:
	input:
		outdir + "/bam/{sample}.sorted.bam"
	output:
		outdir + "/bam/{sample}.sorted.bam.bai"
	threads:
		threads
	shell:
		"samtools index -@ {threads} {input}"

rule bam_index_picard:
	input:
		outdir + "/bam/{sample}.picard.bam"
	output:
		outdir + "/bam/{sample}.picard.bam.bai"
	threads:
		threads
	shell:
		"samtools index -@ {threads} {input}"

rule read1:
	input:
		outdir + "/bam/{sample}.picard.bam"
	output:
		outdir + "/read1/{sample}.picard.bam.read1.bam"
	shell:
		"bamtools filter -in {input} -out {output} -isFirstMate true"
rule bam_index_1:
	input:
		outdir + "/read1/{sample}.picard.bam.read1.bam"
	output:
		outdir + "/read1/{sample}.picard.bam.read1.bam.bai"
	threads:
		threads
	shell:
		"samtools index -@ {threads} {input}"
