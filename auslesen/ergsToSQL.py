#!/usr/bin/env python3

""" Dokumentation
Durch dieses Skript wird eine Datei erstellt, indem die Daten der Fragebögen
in SQL-Code stehen.
"""
 
with open("./presql.txt", "r") as f:
    lines = f.read().splitlines()
file = open("./ergs.sql", "w")

anz_lines = len(lines)
i = 0

while i < anz_lines:
    data = lines[i].split(";")
    answers = data[1:]
    print(f"wir sind bei Vl {data[0]}")
    
    #gucken, ob ein Vl-Bogen vorliegt (Vorder- und Rueckseite sind da)
    next_data = lines[i+1].split(";")
    if (i+1 < anz_lines) and (int(data[0]) == int(next_data[0])) and (int(data[2].split(',')[0])==1 and int(next_data[2].split(',')[0])==39):
        answers_page_2 = next_data[2:]
        answers = answers + answers_page_2

        for j in range(1,63):
            if j < len(answers):
                if int(answers[j].split(',')[0]) != j:
                    answers.insert(j,str(j))
            else:
                answers.append(str(j))

        sql_line = "INSERT INTO vorlesungsbogen VALUES (NULL, "
        sql_line += f"\'{str(int(data[0]))}\', " # modulID
        
        for j in range(1,17):   #studienfach
            if str(j) in answers[1].split(',')[1:]:
                sql_line += "\'1\', "
            else:
                sql_line += "\'0\', "

        sql_line += f"\'{str(answers[2].split(',')[1])}\', " #fachsem

        for j in range(1,7):   #gruende
            if str(j) in answers[3].split(',')[1:]:
                sql_line += "\'1\', "
            else:
                sql_line += "\'0\', "

        for j in range(1,5): # teilnahme
            if str(j) in answers[4].split(',')[1:]:
                sql_line += f"\'{str(j)}\', "
        
        for j in range(5,11): # teilnahmegrund
            if str(j) in answers[4].split(',')[1:]:
                sql_line += "\'1\', "
            else:
                sql_line += "\'0\', "

        for j in range(1,7): # aufwand modul
            if str(j) in answers[5].split(',')[1:]:
                sql_line += f"\'{str(j)}\', "

        for j in range(7,13): # aufwand alle module
            if str(j) in answers[5].split(',')[1:]:
                sql_line += f"\'{str(j-6)}\', "

        sql_line += f"\'{str(answers[6].split(',')[1])}\', " # aufwand

        for j in range(7,17):
            sql_line += f"\'{str(answers[j].split(',')[1])}\', " # frage 7 bis 16

        for j in range(17,27):
            sql_line += f"\'{str(answers[j].split(',')[1])}\', " # frage 17 bis 26

        sql_line += f"\'{str(answers[27].split(',')[1])}\', " # tempo

        sql_line += f"\'{str(answers[28].split(',')[1])}\', " # tafelbenutzung

        if answers[28].split(',')[1]=="1":
            for j in range(29,33):
                sql_line += f"\'{str(answers[j].split(',')[1])}\', " # frage 29 bis 32
        else:
            for j in range(29,33):
                sql_line += "\'\', " # frage 29 bis 32

        sql_line += f"\'{str(answers[33].split(',')[1])}\', " # beamerverwendung

        if answers[33].split(',')[1]=="1":
            for j in range(34,39):
                sql_line += f"\'{str(answers[j].split(',')[1])}\', " # frage 34 bis 38
        else:
            for j in range(34,39):
                sql_line += "\'\', " # frage 34 bis 38

        sql_line += f"\'{str(answers[39].split(',')[1])}\', " # skript

        if answers[39].split(',')[1]=="1":
            for j in range(40,44):
                sql_line += f"\'{str(answers[j].split(',')[1])}\', " # frage 34 bis 38
        else:
            for j in range(40,44):
                sql_line += "\'\', " # frage 34 bis 38


        sql_line += f"\'{str(answers[44].split(',')[1])}\', " # uebungsteilnahme

        if answers[44].split(',')[1]=="1":   
            sql_line += f"\'{str(answers[45].split(',')[1])}\', " # uebungsleiter

            for j in range(1,4): # teilnahme uebung
                if str(j) in answers[46].split(',')[1:]:
                    sql_line += f"\'{str(j)}\', "

            for j in range(4,10): # teilnahmegrund uebung
                if str(j) in answers[46].split(',')[1:]:
                    sql_line += "\'1\', "
                else:
                    sql_line += "\'0\', "

            if not("3" in answers[46].split(',')[1:]): # falls uebungsteilnahme nicht "nie"
                for j in range(47,54):
                    sql_line += f"\'{str(answers[j].split(',')[1])}\', " # frage 47 bis 53

                sql_line += f"\'{str(answers[54].split(',')[1])}\', " # uebungstempo
            else:
                for j in range(47,55):
                    sql_line += "\'\', " # frage 47 bis 54

        else:
            sql_line += "\'\', " # kein uebungsleiter

            sql_line += "\'\', " # teilnahme uebung

            for j in range(4,10): # teilnahmegrund uebung
                sql_line += "\'\', "

            for j in range(47,54):
                sql_line += "\'\', " # frage 47 bis 53

            sql_line += "\'\', " # uebungstempo


        sql_line += f"\'{str(answers[55].split(',')[1])}\', " # uebungsaufgaben angeboten

        if answers[55].split(',')[1]=="1":
            for j in range(1,4): # uebungsaufgaben bearbeitet
                if str(j) in answers[56].split(',')[1:]:
                    sql_line += f"\'{str(j)}\', "

            for j in range(4,10): # grund fuer bearbeitung
                if str(j) in answers[56].split(',')[1:]:
                    sql_line += "\'1\', "
                else:
                    sql_line += "\'0\', "

            if not("3" in answers[56].split(',')[1:]): # falls beabeitung nicht "nie"
                for j in range(57,62):
                    sql_line += f"\'{str(answers[j].split(',')[1])}\', " # frage 57 bis 61

                sql_line += "'"+str(answers[62].split(',')[1])+"');" # schwierigkeitsgrad aufgaben
            else:
                for j in range(57,62):
                    sql_line += "\'\', " # frage 57 bis 61
                sql_line += "'');"
        else:
            sql_line += "\'\', " # keine teilnahme

            for j in range(6):
                sql_line += "\'\', "
            
            for j in range(57,62):
                sql_line += "\'\', "
            sql_line += "'');"

        file.write(sql_line+"\n")
        i += 2
    
    # Abarbeitung der Seminarboegen
    elif answers[1].split(',')[0]=="1":
        
        for j in range(1,121): # etwas verschwendung, erspart aber dictionary
            if j<len(answers):
                if int(answers[j].split(',')[0]) != j:
                    answers.insert(j,str(j))
            else:
                answers.append(str(j))

        sql_line = "INSERT INTO seminarbogen VALUES (NULL, "
        sql_line += f"\'{str(int(data[0]))}\', " # modulID
        
        for j in range(1,17):   #studienfach
            if str(j) in answers[1].split(',')[1:]:
                sql_line += "\'1\', "
            else:
                sql_line += "\'0\', "

        sql_line += f"\'{str(answers[2].split(',')[1])}\', " #fachsem
        
        for j in range(1,7):   #gruende
            if str(j) in answers[3].split(',')[1:]:
                sql_line += "\'1\', "
            else:
                sql_line += "\'0\', "

        for j in range(1,5): # teilnahme
            if str(j) in answers[4].split(',')[1:]:
                sql_line += f"\'{str(j)}\', "
        
        for j in range(5,11): # teilnahmegrund
            if str(j) in answers[4].split(',')[1:]:
                sql_line += "\'1\', "
            else:
                sql_line += "\'0\', "

        for j in range(1,7): # aufwand modul
            if str(j) in answers[5].split(',')[1:]:
                sql_line += f"\'{str(j)}\', "

        for j in range(7,13): # aufwand alle module
            if str(j) in answers[5].split(',')[1:]:
                sql_line += f"\'{str(j-6)}\', "

        sql_line += f"\'{str(answers[6].split(',')[1])}\', " # aufwand

        for j in range(7,17):
            sql_line += f"\'{str(answers[j].split(',')[1])}\', " # frage 7 bis 16


        for j in range(117,120):
            sql_line += f"\'{str(answers[j].split(',')[1])}\', " # frage 17 bis 19 auf seminarbogen
        sql_line += "'"+str(answers[120].split(',')[1])+"');"

        file.write(sql_line+"\n")
        i += 1
    else:
        i += 1
        
file.close()
