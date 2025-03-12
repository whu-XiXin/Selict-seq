# Selict-seq
----------------------------------------
## Scripts for analysing Selict-seq data ##
----------------------------------------
The tools for analysis data from biochemical method Selict-seq to evaluate genome-wide off-target editing by ABEs. including the basic processing tools for quality control, clean reads mapping, mutation sites extracting, remove SNP background and so on.

----------------------------------------
### The link address:
Github: https://github.com/whu-XiXin/Selict-seq/
-----------------------------------------

### Data analysis process
------------------------------------	

**Create snakemake config file for 1_DNAMapping.py**

```

# samples list
samples:
  - sample1
  - sample2
  - sample3

# threads conut 
threads: 8

# Bowtie2 index path
bowtie2_index: "/genomes/hg19/index/bowtie2/hg19"

# input data path
path: "/data/raw/"

#genome_size
genome_size: 3099734149

```

**Runing 1_DNAMapping.py**

Before running 1_DNAMapping.py, please install snakemake, TrimGalore, bowtie2, samtools, and other necessary software on your own. Then, use the bowtie2-build command to construct an index with the reference genome.

```
snakemake --cores 8
```

**Create snakemake config file for 2_Mutation.py**

```
# samples list
samples:
  - sample1
  - sample2
  - sample3

# threads conut 
threads: 8

#genome_size
genome_size: 3099734149

```
**Runing 2_Mutation.py**

Before running 2_Mutation.py, please download SNP site information from public databases on your own, which will be used to remove SNP sites from the mutation sites.

```
snakemake --cores 8
```



