#!/usr/bin/env runsnakemake
configfile: "config.yaml"

samples = config["samples"]
threads = config["threads"]
indir = config["path"]
outdir = "results"
genome_size = config["genome_size"]

rule all:
	input:
#		expand(outdir + "/mutation/{sample}.sorted.mut", sample = samples),
		expand(outdir + "/mutation_read1/{sample}.sorted.bam.read1.bam.mut", sample = samples),
		expand(outdir + "/mutation_read1/{sample}.sorted.bam.read1.bam.mut.stat", sample = samples),
		expand(outdir + "/mutation_read1/{sample}.sorted.bam.read1.bam.mut.stat.nonSNP.txt", sample = samples),

rule mutaion_stat:
	input:
		outdir + "/bam/{sample}.sorted.bam"
	output:
		outdir + "/mutation/{sample}.sorted.mut"
	params:
		"/home/sqhan/data_big/sqhan/snakemake_pipline/01.DNA/DNA_I/stat_DNA_I.py"
	shell:
		"python {params} {input} {genome_size} > {output}"


rule mutaion_stat_read1:
	input:
		outdir + "/read1/{sample}.picard.bam.read1.bam"
	output:
		outdir + "/mutation_read1/{sample}.sorted.bam.read1.bam.mut"
	params:
		"/home/sqhan/data_big/sqhan/snakemake_pipline/01.DNA/DNA_I/stat_DNA_I.py"
	shell:
		"python {params} {input} {genome_size} > {output}"

rule mut2stat:
	input:
		outdir + "/mutation_read1/{sample}.sorted.bam.read1.bam.mut"
	output:
		outdir + "/mutation_read1/{sample}.sorted.bam.read1.bam.mut.stat"
	shell:
		"python ~/bin_python/find_error_screen_DNA_I.py {input} > {output}"

rule remove_snp:
	input:
		outdir + "/mutation_read1/{sample}.sorted.bam.read1.bam.mut.stat"
	output:
		outdir + "/mutation_read1/{sample}.sorted.bam.read1.bam.mut.stat.nonSNP.txt"
	shell:
		"python /home/sqhan/bin_python/remove_snp.py {input} /dat99/zhouxiang/sqhan/00.DATABASE/hg38/SNP/SNP151/snp151.txt > {output}"


