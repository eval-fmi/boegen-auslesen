#!/usr/bin/env python3

vls = set()

file = open("./ergs.txt", "r")
for line in file:
    hilf = line.split(";",2)
    vls.add(hilf[0])
file.close()

vls = list(vls)
vls.sort()

vlsdic = {}

for vl in vls:
    vlsdic.update({int(vl) : []})

file = open("./ergs.txt", "r")
for line in file:
    hilf = line.split(";",2)
    vlsdic[int(hilf[0])] += [hilf[2]]
file.close()

for v in vlsdic:
    vlsdic[v].sort()

for v in vlsdic:
    isvl = False
    for line in vlsdic[v]:
        if line[0:2]=="39":
            isvl = True
            break
    if(isvl):
        l = len(vlsdic[v])
        hilf = l*[""]

        for k in range(l//2):
            hilf[2*k] = vlsdic[v][k]
            hilf[2*k+1] = vlsdic[v][l//2 + k]
        vlsdic[v] = hilf


file = open("./presql.txt", "w")
for s in vlsdic:
    for k in range(len(vlsdic[s])):
        file.write(str(s)+";"+str(k)+";"+vlsdic[s][k].strip()+"\n")
file.close()
