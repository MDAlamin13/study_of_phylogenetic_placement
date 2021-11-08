import sys
import os
from ete3 import Tree
from Bio import SeqIO
import subprocess

def create_backbone(model_tree,query,output_file,num_taxa):
    prune_list=[]
    for i in range(1,num_taxa+1):
        if(str(i)!=query):
            prune_list.append(str(i))
    t=Tree(model_tree)
    t.prune(prune_list,preserve_branch_length=True)
    t.write(format=5, outfile=output_file)

#def ref_query_split(file,query,outgrp,q_file,ref_file):
def ref_query_split(file,query,q_file,ref_file):    
    FastaFile = open(file, 'rU')
    seqLen=0
    qf=open(q_file,'w')
    rf=open(ref_file,'w')
    for rec in SeqIO.parse(FastaFile, 'phylip'):
        name = rec.id
        seq = rec.seq
        if (name==query):
            qf.write('>%s\n'%(query))
            qf.write('%s'%seq)
        #elif (name==outgrp):
        #    continue
        else:
            rf.write('>%s\n'%(name))
            rf.write('%s\n'%(seq)) 
    qf.close()
    rf.close()   
    
#ms_command_file=sys.argv[1]
model_tree_file=sys.argv[1]
query=sys.argv[2]
rep=int(sys.argv[3])
num_taxa=sys.argv[4]


available_loci=20
use_locus_amount=10

#ms_command=''
model_tree=''
'''
with open(ms_command_file,'r') as mscf:
    for line in mscf:
        ms_command=line.split('\n')[0]
        break
'''
with open(model_tree_file,'r') as mtf:
    for line in mtf:
        model_tree=line.split('\n')[0]
        break    

    
#command=ms_command.split('>')[0]    #reduced the number of gene trees from 1000 to 100
#outgroup=command.split(' ')[1]
treefile='treefile_'+str(query)+'_'+str(rep)
dir='/mnt/home/alaminmd/research/metagenomics/placement/reticular_node/'
treefile_main=dir+'true-gene-trees/true_gene_trees_with_bl_'+num_taxa+'_'+str(rep)+'.tree'
tree_cmd='head -'+str(available_loci)+' '+treefile_main+' > '+treefile
os.system(tree_cmd)
#ms_c=command+' | tail -n +4 | grep -v // >'+treefile
#print(ms_c)
#print("Executing MS..")
#os.system(ms_c)
#print("MS finished..")

seq_file='all_aln_'+str(query)+'_'+str(rep)+'.fasta'
seq_cmd='seq-gen -mHKY -l 100000 -s 0.2 < '+treefile+' > '+seq_file
os.system(seq_cmd)
#msa_file='all_aln_'+str(query)+'_'+str(rep)+'.fasta'
#concat_cmd='python concat_all_loci.py '+seq_file+' '+msa_file
#os.system(concat_cmd)

cmd='python separate_loci.py '+seq_file+' '+num_taxa+' '+str(available_loci)+' '+str(use_locus_amount)
os.system(cmd)
backbone_tree_rooted='backbone_rooted_'+str(query)+'_'+str(rep)+'.tree'
create_backbone(model_tree,query,backbone_tree_rooted,int(num_taxa))

for locus in range(1,use_locus_amount+1):
    msa_file=seq_file.split('.')[0]+'_locus_'+str(locus)+'.fasta'
    q_file='query_'+str(query)+'_locus_'+str(locus)+'_'+str(rep)+'.fasta'
    ref_file='ref_'+str(query)+'_locus_'+str(locus)+'_'+str(rep)+'.fasta'
    #ref_query_split(msa_file,query,outgroup,q_file,ref_file)
    ref_query_split(msa_file,query,q_file,ref_file)
    #backbone_tree_unrooted='backbone_unrooted_'+str(query)+'_'+str(rep)+'.tree'

    rax_rees_cmd='raxmlHPC -f e -t '+backbone_tree_rooted+' -m GTRGAMMA -s '+ ref_file+' -n backbone_'+str(query)+'_locus_'+str(locus)+'_'+str(rep)
    os.system(rax_rees_cmd)
    ref_package=str(query)+'_locus_'+str(locus)+'_'+str(rep)+'.refpkg'
    ref_package_cmd='taxit create -l DNA_contigs -P '+ref_package+' --aln-fasta '+ref_file+' --tree-stats RAxML_info.backbone_'+str(query)+'_locus_'+str(locus)+'_'+str(rep)+' --tree-file RAxML_result.backbone_'+str(query)+'_locus_'+str(locus)+'_'+str(rep)
    os.system(ref_package_cmd)

    query_sequences='fragment_queries_'+str(query)+'_locus_'+str(locus)+'_'+str(rep)+'.fasta'
    cmd='python generate_fragments.py '+q_file+' '+query_sequences+' 250 60 10' #fragment mean,std,num
    os.system(cmd)
    '''
    final_aln='mafft_aln_'+str(query)+'_'+str(rep)+'.fasta'
    mafft_cmd='mafft --auto --addfragments '+q_file+' --thread -1 '+ref_file+' > '+final_aln
    os.system(mafft_cmd)
    '''
    final_aln='clustal_aln_'+str(query)+'_locus_'+str(locus)+'_'+str(rep)+'.fasta'
    clustal_cmd='clustalw2 -PROFILE1='+ref_file+' -PROFILE2='+query_sequences+' -SEQUENCES -OUTFILE='+final_aln+' -OUTPUT=FASTA'
    os.system(clustal_cmd)

    pplacer_cmd='pplacer -c '+ref_package+' '+ final_aln
    os.system(pplacer_cmd)

    jplace_temp='clustal_aln_'+str(query)+'_locus_'+str(locus)+'_'+str(rep)+'.jplace'
    jplace_pplacer='pplacer_'+str(query)+'_locus_'+str(locus)+'_'+str(rep)+'.jplace'
    cmd='mv '+jplace_temp+' '+jplace_pplacer
    os.system(cmd)

    placement_tree='pplacer_placement_'+str(query)+'_locus_'+str(locus)+'_'+str(rep)+'.tree'
    guppy_cmd='guppy tog '+jplace_pplacer+' -o '+placement_tree
    os.system(guppy_cmd)
