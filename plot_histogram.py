import sys
dist_file=sys.argv[1]
dict={}
with open(dist_file,'r') as inp:
    for line in inp:
        spaced=line.split(" ")
        for key in spaced:
            t=key.split('\n')[0]
            if t not in dict:
                dict[t]=0
            else:
                dict[t]+=1
print(dict)                     