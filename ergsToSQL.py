#!/usr/bin/env python3

 
with open("./presql.txt", "r") as f:
    lines = f.read().splitlines()
file = open("./ergs.sql", "w")

n=len(lines)
i = 0

while i<n:
    line = lines[i].split(";")
    a = line[1:]


    if (i+1<n) and (int(line[0])==int(lines[i+1].split(";")[0])) and (int(line[2].split(",")[0])==1 and int(lines[i+1].split(";")[2].split(",")[0])==39): #falls vorder- und rueckseite eines vl-bogens 
        nextline = lines[i+1].split(";")
        b = nextline[2:]
        a = a+b



        for j in range(1,63):
            if j<len(a):
                if int(a[j].split(",")[0]) != j:
                    a.insert(j,str(j))
            else:
                a.append(str(j))

        sqlline = "INSERT INTO vorlesungsbogen VALUES (NULL, "
        sqlline +="'"+str(int(line[0]))+"', " # modulID
        
        for j in range(1,17):   #studienfach
            if str(j) in a[1].split(",")[1:]:
                sqlline +="'1', "
            else:
                sqlline +="'0', "

        sqlline +="'"+str(a[2].split(",")[1])+"', " #fachsem

        for j in range(1,7):   #gruende
            if str(j) in a[3].split(",")[1:]:
                sqlline +="'1', "
            else:
                sqlline +="'0', "

        for j in range(1,5): # teilnahme
            if str(j) in a[4].split(",")[1:]:
                sqlline +="'"+str(j)+"', "
        
        for j in range(5,11): # teilnahmegrund
            if str(j) in a[4].split(",")[1:]:
                sqlline +="'1', "
            else:
                sqlline +="'0', "

        for j in range(1,7): # aufwand modul
            if str(j) in a[5].split(",")[1:]:
                sqlline +="'"+str(j)+"', "

        for j in range(7,13): # aufwand alle module
            if str(j) in a[5].split(",")[1:]:
                sqlline +="'"+str(j-6)+"', "

        sqlline +="'"+str(a[6].split(",")[1])+"', " # aufwand

        for j in range(7,17):
            sqlline += "'"+str(a[j].split(",")[1])+"', " # frage 7 bis 16

        for j in range(17,27):
            sqlline += "'"+str(a[j].split(",")[1])+"', " # frage 17 bis 26

        sqlline +="'"+str(a[27].split(",")[1])+"', " # tempo

        sqlline +="'"+str(a[28].split(",")[1])+"', " # tafelbenutzung

        if a[28].split(",")[1]=="1":
            for j in range(29,33):
                sqlline += "'"+str(a[j].split(",")[1])+"', " # frage 29 bis 32
        else:
            for j in range(29,33):
                sqlline += "'', " # frage 29 bis 32

        sqlline +="'"+str(a[33].split(",")[1])+"', " # beamerverwendung

        if a[33].split(",")[1]=="1":
            for j in range(34,39):
                sqlline += "'"+str(a[j].split(",")[1])+"', " # frage 34 bis 38
        else:
            for j in range(34,39):
                sqlline += "'', " # frage 34 bis 38

        sqlline +="'"+str(a[39].split(",")[1])+"', " # skript

        if a[39].split(",")[1]=="1":
            for j in range(40,44):
                sqlline += "'"+str(a[j].split(",")[1])+"', " # frage 34 bis 38
        else:
            for j in range(40,44):
                sqlline += "'', " # frage 34 bis 38


        sqlline +="'"+str(a[44].split(",")[1])+"', " # uebungsteilnahme

        if a[44].split(",")[1]=="1":   
            sqlline += "'"+str(a[45].split(",")[1])+"', " # uebungsleiter

            for j in range(1,4): # teilnahme uebung
                if str(j) in a[46].split(",")[1:]:
                    sqlline +="'"+str(j)+"', "

            for j in range(4,10): # teilnahmegrund uebung
                if str(j) in a[46].split(",")[1:]:
                    sqlline +="'1', "
                else:
                    sqlline +="'0', "

            if not("3" in a[46].split(",")[1:]): # falls uebungsteilnahme nicht "nie"
                for j in range(47,54):
                    sqlline += "'"+str(a[j].split(",")[1])+"', " # frage 47 bis 53

                sqlline +="'"+str(a[54].split(",")[1])+"', " # uebungstempo
            else:
                for j in range(47,55):
                    sqlline += "'', " # frage 47 bis 54

        else:
            sqlline +="'', " # kein uebungsleiter

            sqlline +="'', " # teilnahme uebung

            for j in range(4,10): # teilnahmegrund uebung
                sqlline +="'', "

            for j in range(47,54):
                sqlline += "'', " # frage 47 bis 53

            sqlline +="'', " # uebungstempo


        sqlline +="'"+str(a[55].split(",")[1])+"', " # uebungsaufgaben angeboten

        if a[55].split(",")[1]=="1":
            for j in range(1,4): # uebungsaufgaben bearbeitet
                if str(j) in a[56].split(",")[1:]:
                    sqlline +="'"+str(j)+"', "

            for j in range(4,10): # grund fuer bearbeitung
                if str(j) in a[56].split(",")[1:]:
                    sqlline +="'1', "
                else:
                    sqlline +="'0', "

            if not("3" in a[56].split(",")[1:]): # falls beabeitung nicht "nie"
                for j in range(57,62):
                    sqlline += "'"+str(a[j].split(",")[1])+"', " # frage 57 bis 61

                sqlline +="'"+str(a[62].split(",")[1])+"');" # schwierigkeitsgrad aufgaben
            else:
                for j in range(57,62):
                    sqlline += "'', " # frage 57 bis 61
                sqlline += "'');"
        else:
            sqlline +="'', " # keine teilnahme

            for j in range(6):
                sqlline +="'', "
            
            for j in range(57,62):
                sqlline += "'', "
            sqlline += "'');"

        file.write(sqlline+"\n")
        i+=2
            
    elif a[1].split(",")[0]=="1": # Seminarbogen
        
        for j in range(1,121): # etwas verschwendung, erspart aber dictionary
            if j<len(a):
                if int(a[j].split(",")[0]) != j:
                    a.insert(j,str(j))
            else:
                a.append(str(j))

        sqlline = "INSERT INTO seminarbogen VALUES (NULL, "
        sqlline +="'"+str(int(line[0]))+"', " # modulID
        
        for j in range(1,17):   #studienfach
            if str(j) in a[1].split(",")[1:]:
                sqlline +="'1', "
            else:
                sqlline +="'0', "

        sqlline +="'"+str(a[2].split(",")[1])+"', " #fachsem

        for j in range(1,7):   #gruende
            if str(j) in a[3].split(",")[1:]:
                sqlline +="'1', "
            else:
                sqlline +="'0', "

        for j in range(1,5): # teilnahme
            if str(j) in a[4].split(",")[1:]:
                sqlline +="'"+str(j)+"', "
        
        for j in range(5,11): # teilnahmegrund
            if str(j) in a[4].split(",")[1:]:
                sqlline +="'1', "
            else:
                sqlline +="'0', "

        for j in range(1,7): # aufwand modul
            if str(j) in a[5].split(",")[1:]:
                sqlline +="'"+str(j)+"', "

        for j in range(7,13): # aufwand alle module
            if str(j) in a[5].split(",")[1:]:
                sqlline +="'"+str(j-6)+"', "

        sqlline +="'"+str(a[6].split(",")[1])+"', " # aufwand

        for j in range(7,17):
            sqlline += "'"+str(a[j].split(",")[1])+"', " # frage 7 bis 16


        for j in range(117,120):
            sqlline += "'"+str(a[j].split(",")[1])+"', " # frage 17 bis 19 auf seminarbogen
        sqlline += "'"+str(a[120].split(",")[1])+"');"

        file.write(sqlline+"\n")
        i+=1
    else:
        i+=1
        
file.close()
