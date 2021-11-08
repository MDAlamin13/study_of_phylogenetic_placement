import sys
import os
filename=sys.argv[1]
num_taxa=int(sys.argv[2])
present_num_locus=int(sys.argv[3])
extract_locus_num=int(sys.argv[4])

locus=1
total_line=(num_taxa+1)*present_num_locus
for break_point in range(num_taxa+1,total_line+1,num_taxa+1):
    newfile=filename.split('.')[0]+'_locus_'+str(locus)+'.fasta'
    cmd='head -'+str(break_point)+' '+filename+' | '+'tail -'+str(num_taxa+1)+' > '+newfile
    os.system(cmd)
    locus+=1
    if(locus>extract_locus_num):
        break

         
