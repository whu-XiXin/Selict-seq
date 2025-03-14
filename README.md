# Selict-seq
----------------------------------------
## Scripts for analysing Selict-seq data ##
----------------------------------------
Tools for analyzing data from the biochemical method Selict-seq to evaluate genome-wide off-target editing by ABEs. including the basic processing tools for quality control, clean reads mapping, mutation sites extracting, remove SNP background and so on.

----------------------------------------
### The link address:
Github: https://github.com/whu-XiXin/Selict-seq/
-----------------------------------------

### Data analysis process
------------------------------------	

**Create snakemake config file for 1_DNAMapping.py**

```

# Sample list
samples:
  - sample1
  - sample2
  - sample3

# Number of threads
threads: 8

# Bowtie2 index path
bowtie2_index: "/genomes/hg19/index/bowtie2/hg19"

# Input data path
path: "/data/raw/"

# Genome size
genome_size: 3099734149

```

**Runing 1_DNAMapping.py**

Before running 1_DNAMapping.py, please install snakemake, TrimGalore, bowtie2, samtools, and other necessary software on your own. Then, use the bowtie2-build command to construct an index with the reference genome.

```
snakemake --cores 8
```

**Create snakemake config file for 2_Mutation.py**

```
# Sample list
samples:
  - sample1
  - sample2
  - sample3

# Number of threads
threads: 8

# Genome size
genome_size: 3099734149

```

**Running 2_Mutation.py**

Before running 2_Mutation.py, please download SNP site information from public databases on your own, which will be used to remove SNP sites from the mutation sites.

```
snakemake --cores 8
```

**Running 3_Merge_parallel_group.py**

```
python 3_Merge_parallel_group.py -1 {sample1_parallel1}.sorted.bam.read1.bam.mut.stat.nonSNP.txt -2 {sample1_parallel2}.sorted.bam.read1.bam.mut.stat.nonSNP.txt -o {sample1}.merge.sorted.bam.read1.bam.mut.stat.nonSNP.txt
```

**Running 4_Merge_group_rmBackground.py**

```
python 4_Merge_group_rmBackground.py -i {sample1}.sorted.bam.read1.bam.mut.stat.nonSNP.merge.txt -bg /home/data/backgroundpath -o /output_path/{sample1}.sorted.bam.read1.bam.mut.stat.nonSNP.merge.rmbakeground.txt
```
The BED file generated under the output path represents the editing sites, which can be used as input for downstream data analysis and plotting.

**Running 5_bed-to-art-sgRNA.sh**

In this step, we use the mpmat-to-art-sgRNA.py script from the Detect-seq developed by the Chengqi Yi group for processing.

Before running 5_bed-to-art-sgRNA.sh, please download Detect-seq from (Github: https://github.com/menghaowei/Detect-seq) on your own.

```
bash 5_bed-to-art-sgRNA.sh
```

Then, we obtain the ART file containing information such as the sgRNA sequence, alignment penalty score, and so on. Using this information, we can filter for certain editing sites and plot an sgRNA distribution diagram.


