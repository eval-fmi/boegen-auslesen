#!/usr/bin/env python3

# Wie ist dieses Skript zu benutzen?:
#
# Die Eval-Bögen sollten eingescannt im einem der Formate tiff,gif,jpg,png vorliegen (Graustufen oder monochrom)
# und eine Ausflösung von min ca 300 dpi aufweisen (mit 300 getestet -> Erkennung klappt gut).
# 
# Jede Seite sollte eine eigene Datei sein (keine mehrseitigen Tiffs).
#
# Die erwartete Ordnerstruktur:
# EvalWS1516 ─┬── 001 ─┬── filename1.tiff
#             │        ├── filename2.tiff
#             ¦        ¦ 
#             ¦        └── filenameN1.tiff
#             ├── 002 ─┬── filename1.tiff
#             │        ├── filename2.tiff
#             ¦        ¦ 
#             ¦        └── filenameN2.tiff
#             ¦
#             └── 999 ─┬── filename1.tiff
#                      ├── filename2.tiff
#                      ¦ 
#                      └── filenameN999.tiff 
#            
#
# D.h. jede Vorlesung/Seminar bekommt einen Ordner mit dem Namen der jeweiligen Vorlesungsnummer (3-stellig).
# In diesen Ordnern befinden sich die gescannten Dateien. (Leere Seiten sind kein Problem, leere Vorlesungen ebenfalls).
# Die 2-seitigen Vorlesungsbögen sollten aufsteigend nummeriert sein (Vorderseite ungerade, Rueckseite gerade oder umgekehrt) - die Kopierer in der Fakultaet
# vergeben standardmaessig Namen der Form "20160421091821_001.tif", "20160421091822_002.tif" usw.
# In dieser Form, funktioniert das Skript korrekt. 
# Die Seiten werden automatisch gedreht (keine maneuelle Bearbeitung noetig).
# Das Script erwartet als Parameter den Ordner, welcher alle Vorlesungsordner enthält (im obigen Beispiel:
#   > ./readOutQuestionnaires EvalWS1516.
# Dabei wird die Datei ergs.txt erstellt (und falls vorhanden UEBERSCHRIEBEN!)
#
# Benötigte Programme: Python3 (+übliche Pakete wie numpy), ImageMagick, Tesseract, Levenshtein
#
#


import sys
import numpy as np
from numpy import linalg as LA
from subprocess import call
import os
import tkinter
from phases import *
import multiprocessing
from concurrent import futures

argv=sys.argv

if len(argv)<2:
    sys.exit('Fehlendes Argument.')
elif not os.path.isdir(argv[1]):
    sys.exit(argv[1]+" ist kein Verzeichnis.")

if(argv[1][-1]!="/"):
    argv[1] += "/"

sys.stdout.write("Fortschritt: 0.00%")
toDo = []
VLs = list(os.listdir(argv[1]))
VLs = sorted(VLs,key=str.lower)
for VL in VLs:
    if os.path.isdir(argv[1]+VL):
        FBs = list(os.listdir(argv[1]+VL))
        FBs = sorted(FBs,key=str.lower)
        for FB in FBs:
            split = FB.rpartition('.')
            if split[-1].lower() in ['tif','tiff','gif','jpg','jpeg','png']:
                toDo = toDo + [argv[1]+VL+"/"+FB]

toDoCount = len(toDo)

counter = 0
toDoAgain = []
toDoManually = [] 
unknowns = []
knowns = []


# mache parallel-rechnend phase 1:
for leftborder in [0,1]:
    for rightborder in [0,1]:
        for topborder in [0,1]:
            for bottomborder in [0,1]:
                with futures.ThreadPoolExecutor(max_workers=8) as e:
                    fs = {e.submit(phase1, file, leftborder,rightborder,topborder,bottomborder): file for file in toDo}
                    for f in futures.as_completed(fs):
                        p = f.result()
                        if p[0]=='help':
                            toDoAgain.append(p[1])
                        elif p[0]=='unknown':
                            unknowns.append(p)
                        elif p[0]!='empty':
                            knowns.append(p)
                            counter+=1
                            sys.stdout.write("\rFortschritt: "+"{0:.2f}".format(100*counter/2/toDoCount)+"%")
                        else:
                            counter+=1
                            sys.stdout.write("\rFortschritt: "+"{0:.2f}".format(100*counter/2/toDoCount)+"%")
                toDo = toDoAgain
                toDoAgain = []

toDoManually = toDo


anzahl=len(toDoManually)
for Questionnaire in toDoManually:
    erg=phase1M(Questionnaire,anzahl)
    anzahl-=1
    if erg == []:
        counter+=1
    else:
        if erg[0] == "unknown":
            unknowns.append(erg)
        else:
            knowns.append(erg)
            counter += 1
            sys.stdout.write("\rFortschritt: "+"{0:.2f}".format(100*counter/2/toDoCount)+"%")

toDoManually = []

dic = {}
for known in knowns:
    vl = known[1].split("/")[-2]                        # liefert VL-Nummer (Name des Oberordners)
    dat = known[1].split("/")[-1].split(".")[0]        # liefert Dateiname ohne Endung
    if int(dat[-1])%2 == 0:
        dic[vl] = known[0]+":even"
    else:
        dic[vl] = known[0]+":odd"
for unknown in unknowns:
    vl = unknown[1].split("/")[-2]                      # liefert VL-Nummer (Name des Oberordners)
    dat = unknown[1].split("/")[-1].split(".")[0]      # liefert Dateiname ohne Endung
    if vl in dic:
        if (dic[vl].split(":")[-1]=="even" and int(dat[-1])%2 == 0) or (dic[vl].split(":")[-1]=="odd" and int(dat[-1])%2 == 1):
            unknown[0]=dic[vl].split(":")[0]
        elif dic[vl].split(":")[0]=="Vorlesung1":
            unknown[0]="Vorlesung2"
        elif dic[vl].split(":")[0]=="Vorlesung2":
            unknown[0]="Vorlesung1"
        else:
            unknown[0]="Seminar"
        knowns.append(unknown)
        counter+=1
        sys.stdout.write("\rFortschritt: "+"{0:.2f}".format(100*counter/2/toDoCount)+"%")
    else:
        toDoManually.append(unknown[1:])


anzahl=len(toDoManually)
for Questionnaire in toDoManually:
    erg=phase2M(Questionnaire,anzahl)
    anzahl-=1
    if erg == []:
        counter+=1
    else:
        knowns.append(erg)
        counter+=1
        sys.stdout.write("\rFortschritt: "+"{0:.2f}".format(100*counter/2/toDoCount)+"%")

finalList=[]

for known in knowns:
    typ = known[0]
    Questionnaire = known[1]
    origin = known[2]
    width = known[3]
    height = known[4]
    vl = Questionnaire.split("/")[-2] # VL Nummer 
    bogennummer = Questionnaire.split("/")[-1].split(".")[0] # Bogennummer 
    while(not bogennummer.isnumeric()):
        bogennummer = bogennummer[1:]
    s= ""
    for e in phase2(typ,Questionnaire,origin,width,height):
        s=s+";"+e
    if s!="":
        finalList+=[[vl,typ,bogennummer+s]]
    counter+=1
    sys.stdout.write("\rFortschritt: "+"{0:.2f}".format(100*counter/(len(knowns)+toDoCount))+"%")

finalList.sort(key=lambda x: x[1]) # sortiere nach typ 
finalList.sort(key=lambda x: x[0]) # sortiere nach vl nummer (sort ist stabil)

file = open("./ergs.txt", "w")
for s in finalList:
    file.write(s[0]+";"+s[2]+"\n")
file.close()


print('\nFertig.')

