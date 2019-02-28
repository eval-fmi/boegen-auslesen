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
# Folgende Abkürzungen werden verwendet:
# fb: Fragebogen
# fbs:  Fragebögen
# vl:  Vorlesung
# vls: Vorlesungen


import sys
import os
from subprocess import call
import logging
import multiprocessing
import tkinter
from concurrent import futures

# TODO kann ich das rausnehmen?
from auslesen.phases import phase1, phase1M, phase2, phase2M

logging.basicConfig(filename=f'{(__file__)[:-3]}.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s', datefmt = "%H:%M-%x")
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())


def fbs_vorbereiten(root_ordner):
    """ entnimmt die Fragebögen aus den Ordnern und bereitet sie für
        Bearbeitung vor. root_ordner vom Typ str
    """

    logger.info("Fragebögen werden vorbereitet")
    fbs_liste = []

    if not os.path.isdir(root_ordner):
        logger.error(root_ordner + " ist kein Verzeichnis.", exec = True)
    if not root_ordner.endswith("/"):
        root_ordner += "/"

    # sortiert die Fragebögen in dem Root-Ordner aus den jeweiligen Ordnern und
    unsortierte_vls = list(os.listdir(root_ordner))
    sortierte_vls = sorted(unsortierte_vls, key=str.lower)
    for vl_num in sortierte_vls:
        vl_pfad = root_ordner + vl_num
        if os.path.isdir(vl_pfad):
            fbs = list(os.listdir(vl_pfad))
            fbs = sorted(fbs, key=str.lower)
            for fb in fbs:
                split = fb.rpartition('.')
                if split[-1].lower() in ['tif','tiff','gif','jpg','jpeg','png']:
                    fbs_liste.append(vl_pfad +"/"+ fb)

    logger.info("Es gibt " +str(len(fbs_liste))+ " Fragebögen.")
    return fbs_liste

def phase1_durchfuehren(fbs_liste):
    """ Führt die erste Phase (phase1) auf allen Fragebögen aus
        fbs_liste beinhaltet die die Pfade der einzelnen Fragebögen
    """
    fbs_nacharbeiten_liste = [] 
    fbs_unbekannt_liste = []
    fbs_bekannt_liste = []
    # mache parallel-rechnend phase 1
    for leftborder in [0,1]:
        for rightborder in [0,1]:
            for topborder in [0,1]:
                for bottomborder in [0,1]:
                    logger.info(str(leftborder) + str(rightborder) + str(topborder) + str(bottomborder))
                    with futures.ThreadPoolExecutor(max_workers=8) as e:
                        threads = {e.submit(phase1, fb, leftborder,rightborder,topborder,bottomborder): fb for fb in fbs_liste}
                        for thread in futures.as_completed(threads):
                            fb_data = thread.result()
                            if fb_data[0]=='help':
                                fbs_nacharbeiten_liste.append(fb_data[1])
                            elif fb_data[0]=='unknown':
                                fbs_unbekannt_liste.append(fb_data)
                            elif fb_data[0]!='empty':
                                fbs_bekannt_liste.append(fb_data)
                            else:
                                logger.info("Hier war etwas komisch")
                    fbs_liste = fbs_nacharbeiten_liste
                    fbs_nacharbeiten_liste = []

    fbs_nacharbeiten_liste = fbs_liste
    logger.info("Die Phase 1 ist abgeschlossen.")
    # fbs_nacharbeiten_liste durcharbeiten
    anzahl = len(fbs_nacharbeiten_liste)
    for fb in fbs_nacharbeiten_liste:
        clear = False
        while not clear:
            try:
                erg = phase1M(fb, anzahl)
                clear = True
            except TypeError:
                logger.error("Hier ist ein fehler aufgetreten! versuche es erneut", exec =True)
        anzahl -= 1
        
        # füge, wenn es einen Fragebogen gibt, diesen der jeweiligen Liste hinzu
        if erg:  # wird wahr, solange die Liste nicht leer ist
            if erg[0] == "unknown":
                fbs_unbekannt_liste.append(erg)
            else:
                fbs_bekannt_liste.append(erg)

    fbs_nacharbeiten_liste = []

    vls_dict = {}
    for fb in fbs_bekannt_liste:
        vl_num = fb[1].split("/")[-2]  # liefert VL-Nummer (Name des Oberordners)
        name = fb[1].split("/")[-1].split(".")[0]  # liefert Dateiname ohne Endung
        if int(name[-1])%2 == 0:
            vls_dict[vl_num] = fb[0]+":even"
        else:
            vls_dict[vl_num] = fb[0]+":odd"

    for fb in fbs_unbekannt_liste:
        vl_num = fb[1].split("/")[-2]  # liefert VL-Nummer (Name des Oberordners)
        name = fb[1].split("/")[-1].split(".")[0]  # liefert Dateiname ohne Endung
        
        # TODO was genau passiert hier?
        if vl_num in vls_dict:
            if (
                (vls_dict[vl_num].split(":")[-1] == "even" and int(name[-1])%2 == 0) 
                or (vls_dict[vl_num].split(":")[-1]=="odd" and int(name[-1])%2 == 1)
                ):
                fb[0]=vls_dict[vl_num].split(":")[0]
            elif vls_dict[vl_num].split(":")[0] == "Vorlesung1":
                fb[0]="Vorlesung2"
            elif vls_dict[vl_num].split(":")[0] == "Vorlesung2":
                fb[0]="Vorlesung1"
            else:
                fb[0]="Seminar"
            fbs_bekannt_liste.append(fb)

        else:
            fbs_nacharbeiten_liste.append(fb[1:])

    logger.info("Phase 2 wird beendet")
    anzahl = len(fbs_nacharbeiten_liste)
    for fb in fbs_nacharbeiten_liste:
        erg = phase2M(fb, anzahl)
        anzahl -= 1
        if erg:
            fbs_bekannt_liste.append(erg)


    logger.info("Phase2M wird beendet")
    fbs_fertig_liste = []

    # TODO was ist der Unterschied zwischen fb und fragebogen?
    # was genau kommt bei phase1 eigentlich zurück?
    for fb in fbs_bekannt_liste:
        typ = fb[0]
        fragebogen = fb[1]
        origin = fb[2]
        width = fb[3]
        height = fb[4]
        vl_num = fragebogen.split("/")[-2]  # VL-Nummer 
        bogennummer = fragebogen.split("/")[-1].split(".")[0]  # Bogennummer 
        while(not bogennummer.isnumeric()):
            bogennummer = bogennummer[1:]
        fb_data = ""
        for erg in phase2(typ, fragebogen, origin, width, height):
            fb_data = fb_data +";"+ erg
        if fb_data != "":
            fbs_fertig_liste.append([vl_num,typ,bogennummer + fb_data])

    fbs_fertig_liste.sort(key = lambda x: x[1]) # sortiere nach typ 
    fbs_fertig_liste.sort(key = lambda x: x[0]) # sortiere nach vl_num (sort ist stabil)

    return fbs_fertig_liste

def daten_speichern(fbs_fertig_liste:list):
    """ speichert die Daten der Fragebögen in der Datei ergs.txt als Zeilen """    
    
    logger.info("Die Daten der Fragebögen werden gepeichert")
    file = open("./ergs.txt", "w")
    for fb_data in fbs_fertig_liste:
        file.write(fb_data[0]+";"+fb_data[2]+"\n")
    file.close()
    logger.info("Die Speicherung ist beendet")

if __name__ == "__main__":
    print("wurde ausgeführt")