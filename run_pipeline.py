import sys
import os
#ms_file=sys.argv[1]
num_taxa=sys.argv[1]
model_tree_file=sys.argv[2]
replicas=[]
for i in range(3,4):
    replicas.append(int(sys.argv[i]))

#ms_commands=[]

querys=[]
for i in range(4,5):
    querys.append(sys.argv[i])
'''   
with open(ms_file,'r') as msf:
    for line in msf:
        ms_commands.append(line)
'''
model_trees=[]
with open(model_tree_file,'r') as mtf:
    for line in mtf:
        model_trees.append(line)        
print(replicas)
print(querys)
#for rep in range(0,5):
for rep in replicas:
    #q=querys[rep]
    q=querys[replicas.index(rep)]
    #msc=ms_commands[rep]
    #mt=model_trees[rep]
    mt=model_trees[rep-1]

    #msc_temp='ms_temp_'+str(rep)
    mt_temp='mt_'+str(rep)
    '''
    with open(msc_temp,'w') as mstemp:
        mstemp.write(msc)
    '''
    with open(mt_temp,'w') as mttemp:
        mttemp.write(mt)


    #command='python pipeline.py '+msc_temp+' '+mt_temp+' '+q+' '+str(rep)
    command='python pipeline.py '+mt_temp+' '+q+' '+str(rep)+' '+num_taxa
    #command='sbatch -A liulab batch.sh '+mt_temp+' '+q+' '+str(rep)+' '+num_taxa
    os.system(command)


    
