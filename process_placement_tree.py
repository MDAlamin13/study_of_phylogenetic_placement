import os
import sys
from ete3 import Tree

refence_tree=sys.argv[1]
placement_tree=sys.argv[2]
num_taxa=int(sys.argv[3])
query=sys.argv[4]
reads=sys.argv[5]
rf_dist_file=sys.argv[6]

ref_t=Tree(refence_tree,format=5)
dist=[]
for r in range(0,int(reads)):
    t=Tree(placement_tree,format=5)
    read_name=query+'_'+str(r)
    node = t.search_nodes(name=read_name)[0]
    node.name=query
    prune_list=[]
    for i in range(1,num_taxa+1):
            prune_list.append(str(i))
    t.prune(prune_list,preserve_branch_length=True)
    robinson = t.robinson_foulds(ref_t,unrooted_trees=True)
    dist.append(str(robinson[0]/robinson[1]))

dist_str=''
for d in dist:
    dist_str+=d+' '        
cmd='echo '+dist_str+' >> '+rf_dist_file
print(cmd)
os.system(cmd)
