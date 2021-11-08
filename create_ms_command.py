import sys
import os
file=sys.argv[1]
num_taxa=sys.argv[2]
outputfile=sys.argv[3]
rep=sys.argv[4]
tree_file=open(file,'r')
new_file=open('new_tree.txt','w')
for line in tree_file:
    for i in range(len(line)):
        if(line[i]=='('):
            new_file.write('%s '%(line[i]))
        elif(line[i]==')'):
            new_file.write(' %s'%(line[i]))
        elif(line[i]==':'):
            new_file.write(' %s '%(line[i]))
        elif(line[i]==','):
            new_file.write(' %s '%(line[i]))
        elif(line[i]==';'):
            new_file.write(' : 0.0 %s'%(line[i]))
        else:
            new_file.write(line[i])
    break                                            
tree_file.close()
new_file.close() 
msfile=open(outputfile,'w')
msfile.write('ms %s 1000 -T -I %s'%(num_taxa,num_taxa))
for i in range(int(num_taxa)):
    msfile.write(' 1')

with open('new_tree.txt','r') as f:
    for line in f:
        splits=line.split(' ')
        stack=[]
        i=0
        while(i<len(splits)):
            if(splits[i]==',' or splits[i]==':' or splits[i]==';'):
                pass
            elif(splits[i]==')'):
                second_branch=stack.pop()
                second_taxa=stack.pop()
                first_branch=float(stack.pop())/2.0
                first_taxa=stack.pop()
                parenthesis=stack.pop()
                i=i+2
                next_branch=splits[i]
                smaller=first_taxa
                bigger=second_taxa
                if(int(second_taxa)<int(first_taxa)):
                    smaller=second_taxa
                    bigger=first_taxa
                msfile.write(' -ej %s %s %s'%(str(first_branch),bigger,smaller))
                new_br_len=float(second_branch)+float(next_branch)
                stack.append(smaller)
                stack.append(str(new_br_len))
            else:
                stack.append(splits[i])    
            i=i+1        

        break
genetrees='genetrees_'+str(rep)
msfile.write(' | tail +4 | grep -v // >%s'%genetrees)
msfile.close()
os.system('rm new_tree.txt')
