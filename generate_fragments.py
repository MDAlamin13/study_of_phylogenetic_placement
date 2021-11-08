import numpy as np
import random
import sys
from Bio import SeqIO
file=sys.argv[1]
output=sys.argv[2]
mu=int(sys.argv[3])
sigma=int(sys.argv[4])
num_frag=int(sys.argv[5])

FastaFile = open(file, 'rU')
seqLen=0
seq=""
seq_name=""
for rec in SeqIO.parse(FastaFile, 'fasta'):
    seq_name = rec.id
    seq = rec.seq
    seqLen = len(rec)
    break

with open(output,'w') as out:
    for i in range(0,num_frag):
        fragment_name=seq_name+'_'+str(i)
        start=random.randint(0, seqLen)
        length=int(np.random.normal(mu,sigma))
        end=min(start+length,seqLen)
        fragment_seq=seq[start:end]
        out.write('>%s\n'%fragment_name)
        out.write('%s\n'%fragment_seq)
