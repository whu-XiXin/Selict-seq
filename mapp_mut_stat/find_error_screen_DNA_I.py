import sys
import collections
from collections import Counter

c = collections.defaultdict(lambda :0)
d = collections.defaultdict(lambda :0)
total_mut = collections.defaultdict(lambda :0)
total_mut_rate = collections.defaultdict(lambda :0)
total_mut_type= collections.defaultdict(list)
filter_sites = collections.defaultdict(lambda :0)
total_mut_type2 = {}
total_cov = collections.defaultdict(list)


d = {}
pos = 1
q = 27

with open(sys.argv[1]) as f:
	for line in f:
		line = line.strip().split('\t')
		if line[7] =='read1' and int(line[5]) - int(line[4]) == pos and int(line[6]) > q and line[8] =='reverse':
			row = line[0] + "\t"+ str(line[1]) + "\t"+ line[2] + "\t" + line[3] +"\t" + line[8] + "\t" +str(line[9])
			
			c[row] +=1
#			print('\t'.join(line))
		elif line[7] =='read1' and int(line[4]) == 2 and int(line[6]) > q and line[8] =='forawrd':
			row = line[0] + "\t"+ str(line[1]) + "\t"+ line[2] + "\t" + line[3] +"\t" + line[8] + "\t" +str(line[9])
			c[row] +=1
#			print('\t'.join(line))

		row = line[0] + "\t"+ str(line[1]) + "\t"+ line[2] + "\t" + line[3] +"\t" + line[8] + "\t" +str(line[9])
		total_mut[row] +=1
		total_cov[line[0] + "\t"+ str(line[1])].append(line[2] + "\t" + line[3])

for k,v in c.items():
	l = k.split('\t')
	cover = float(l[5])
	if v >= 3 and v > 0.2 * cover and cover < 1000 and cover >=5:
		d[k+"\t"+str(v)] = 1



for k,v in total_mut.items():
	
	k = k.split()
	chrID = k[0]
	pos = k[1]
	coverage = float(k[5])
	if coverage == 0:
		print(k,v)
#	print(Counter(total_cov[chrID +"\t"+pos]).most_common(1)[0][0])
	mut_rate = Counter(total_cov[chrID +"\t"+pos]).most_common(1)[0][1]/ coverage
	position  = chrID + "\t" + str(pos)# + "\t" + k[2] + "\t" + k[3]
	position2 = k[2] + "\t" + k[3]
	total_mut_rate[position] = mut_rate
	total_mut_type[position].append(position2)

for k,v in total_mut_type.items():
	v2 = max(v,key=v.count)
	total_mut_type2[k] = v2


for m,n in d.items():
#	print(m,n)
	chrID = m.split('\t')[0]
	position = m.split('\t')[1]
	mut_type = m.split('\t')[2] + "\t" + m.split('\t')[3]
	p = 0 
	for i in range(1,3):
		l1_position = int(position) - i
		r1_position = int(position) + i
		wrong_l1 = chrID + "\t" + str(l1_position)
		wrong_r1 = chrID + "\t" + str(r1_position)
		if wrong_l1 in total_mut_rate and mut_type != total_mut_type2[wrong_l1] and total_mut_rate[wrong_l1] > 0.2:
#			print(wrong_l1,mut_type,total_mut_type2[wrong_l1],total_mut_rate[wrong_l1])
			p = 1
		if wrong_r1 in total_mut_rate and mut_type != total_mut_type2[wrong_r1] and total_mut_rate[wrong_r1] > 0.2:
			p = 1
#			print(wrong_r1,mut_type,total_mut_type2[wrong_r1],total_mut_rate[wrong_r1])
	if p == 0:
		filter_sites[m] = n
	else:
#		print(m)
		continue

#print(total_mut_rate['chr1\t30849747'])
#print(total_mut_rate['chr1\t30849748'])
#print(total_mut_rate['chr1\t30849749'])
for k,v in filter_sites.items():
	print(k)

