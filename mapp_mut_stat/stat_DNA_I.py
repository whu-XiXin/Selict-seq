import sys
import pysam
import numpy as np

samfile = pysam.AlignmentFile(sys.argv[1])

size_path = sys.argv[2]

def get_pileup_database(samfile, size_path):
	sam = samfile
	sizes = dict()
	with open(size_path) as f:
		for line in f:
			row = line.strip("\n").split("\t")
			sizes[row[0]] = int(row[1])
	values = dict()
	for ref in sam.references:
		if ref in sizes:
			length = sizes[ref]
			dat = np.zeros(length)
			for x in sam.pileup(ref, 0, length):
				dat[x.pos] = x.n
			values[ref] = dat
	if 'chrM' in values:
		del values['chrM']

	return values

dict_coverage = get_pileup_database(samfile, size_path)


for reads in samfile.fetch():
	if reads.reference_name == 'chrM':
		continue
	ref_seq = reads.get_reference_sequence()
	ref_len = reads.reference_length
	ref_pos = reads.get_reference_positions(full_length=False)
	read_pos = reads.get_reference_positions(full_length=True)
	read_id = reads.query_name
	read_name = reads.reference_name
	read_start = reads.reference_start
	read_end = reads.reference_end
	read_seq = reads.query_sequence
	read_query = reads.query_qualities
	read_len = str(reads.query_length)
	readpair = 'read1' if reads.is_read1 else 'read2'
	read_strand = 'reverse' if reads.is_reverse else 'forawrd'
	n = -1
	base = ''
	for base in ref_seq:
		n +=1
		if base.islower():
			refbase = base.upper()
			mutation_pos = read_start + n
			mutation_in_reads_pos = read_pos.index(mutation_pos)
			mutation_query = read_query[mutation_in_reads_pos]
			altbase = read_seq[mutation_in_reads_pos]
			coverage = dict_coverage[read_name][mutation_pos]
			new_line = read_name+"\t"+str(mutation_pos+1)+"\t"+refbase+"\t"+altbase+"\t"+str(mutation_in_reads_pos+1)+"\t"+read_len+"\t"+str(mutation_query)+"\t"+readpair+"\t"+read_strand+"\t"+str(coverage)
			print(new_line)
